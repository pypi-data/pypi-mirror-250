from concurrent import futures

from django.core.paginator import Paginator
from django.db import transaction

from drawranflow.models import UploadedFile, Identifiers, Message
import pyshark
import os
from django.conf import settings
import logging
import pandas as pd
import numpy as np
from .utils_sa import INTERFACE_CONFIG_PD
import re
from .statsHandler_sa import computeStats as sh
import concurrent


class FileHandlers:
    def __init__(self):
        pass

    MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)

    @classmethod
    def upload_pcap_file(cls, file, network):
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)

        # Try to get an existing UploadedFile record with the same filename
        try:
            upload_table = UploadedFile.objects.get(filename=file.name)

            # If it exists, delete associated records and the UploadedFile record
            Identifiers.objects.filter(uploaded_file__id=upload_table.id).delete()
            Message.objects.filter(
                identifiers__id__in=Identifiers.objects.filter(uploaded_file__id=upload_table.id).values('id')).delete()
            upload_table.delete()

            # Remove the file from the file system
            if os.path.exists(file_path):
                cls.delete_files(file_path)
        except UploadedFile.DoesNotExist:
            pass

        # Save the new file
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Create or update the UploadedFile record
        uploaded_file_record, created = UploadedFile.objects.get_or_create(filename=file.name, processed=False,
                                                                           network=network)
        uploaded_file_record.save()

        if uploaded_file_record:
            messages = {
                'message_type': 'success',
                'message_text': 'File uploaded successfully',
            }
        else:
            messages = {
                'message_type': 'error',
                'message_text': 'File upload failed',
            }

        return messages

    @classmethod
    def delete_files(cls, file_path):
        # Remove the main file
        os.remove(file_path)
        file_prefix = os.path.basename(file_path).split('.')[0]

        # Find and delete associated files with the same prefix
        for file_name in os.listdir(settings.MEDIA_ROOT):
            if file_name.startswith(file_prefix):
                file_to_delete = os.path.join(settings.MEDIA_ROOT, file_name)
                logging.debug(f"Deleting file: {file_to_delete}")
                os.remove(file_to_delete)

    @classmethod
    def construct_pcap_filter(cls, identifier_data):
        filter_conditions = []

        if identifier_data.c_rnti is not None and identifier_data.c_rnti != '00000' and identifier_data.c_rnti != 'nan' and identifier_data.gnb_du_ue_f1ap_id != 'nan':
            filter_conditions.append(f"(f1ap.C_RNTI=={identifier_data.c_rnti} && "
                                     f"f1ap.GNB_DU_UE_F1AP_ID=={identifier_data.gnb_du_ue_f1ap_id})")

        if identifier_data.gnb_du_ue_f1ap_id != 'nan' and identifier_data.gnb_cu_ue_f1ap_id != 'nan':
            filter_conditions.append(f"(f1ap.GNB_CU_UE_F1AP_ID=={identifier_data.gnb_cu_ue_f1ap_id} && "
                                     f"f1ap.GNB_DU_UE_F1AP_ID=={identifier_data.gnb_du_ue_f1ap_id})")

        if identifier_data.gnb_du_ue_f1ap_id != 'nan' and identifier_data.gnb_cu_ue_f1ap_id == 'nan':
            filter_conditions.append(f"(f1ap.GNB_CU_UE_F1AP_ID=={identifier_data.gnb_cu_ue_f1ap_id})")

        if identifier_data.gnb_cu_cp_ue_e1ap_id != 'nan' and identifier_data.gnb_cu_up_ue_e1ap_id != 'nan':
            filter_conditions.append(f"(e1ap.GNB_CU_CP_UE_E1AP_ID=={identifier_data.gnb_cu_cp_ue_e1ap_id}) or "
                                     f"(e1ap.GNB_CU_CP_UE_E1AP_ID=={identifier_data.gnb_cu_cp_ue_e1ap_id} && "
                                     f"e1ap.GNB_CU_UP_UE_E1AP_ID=={identifier_data.gnb_cu_up_ue_e1ap_id})")

        if identifier_data.gnb_cu_cp_ue_e1ap_id != 'nan' and identifier_data.gnb_cu_up_ue_e1ap_id == 'nan':
            filter_conditions.append(f"(e1ap.GNB_CU_CP_UE_E1AP_ID=={identifier_data.gnb_cu_cp_ue_e1ap_id})")

        if identifier_data.ran_ue_ngap_id != 'nan' and identifier_data.amf_ue_ngap_id != 'nan':
            filter_conditions.append(f"(ngap.RAN_UE_NGAP_ID=={identifier_data.ran_ue_ngap_id}) or "
                                     f"(ngap.RAN_UE_NGAP_ID=={identifier_data.ran_ue_ngap_id} && "
                                     f"ngap.AMF_UE_NGAP_ID=={identifier_data.amf_ue_ngap_id})")

        if identifier_data.ran_ue_ngap_id != 'nan' and identifier_data.amf_ue_ngap_id == 'nan':
            filter_conditions.append(f"ngap.RAN_UE_NGAP_ID =={identifier_data.ran_ue_ngap_id}")

        if identifier_data.xnap_src_ran_id != 'nan':
            filter_conditions.append(f"(xnap.NG_RANnodeUEXnAPID=={identifier_data.xnap_src_ran_id})")

        if identifier_data.xnap_trgt_ran_id != 'nan':
            filter_conditions.append(f"(xnap.NG_RANnodeUEXnAPID=={identifier_data.xnap_trgt_ran_id})")

        filter_string = " or ".join(filter_conditions)
        logging.debug(f'Filter string - {filter_string}')
        # Log or use the generated filter_string as needed

        return filter_string

    @classmethod
    def fetch_identifier_data(cls, row_id):
        logging.debug(f'identifier_data in fetch_identifier_data: {row_id}')
        identifier_data = Identifiers.objects.get(id=row_id)

        return identifier_data

    @classmethod
    def filter_pcap(cls, input_file, filter_string, output_file):
        capture = pyshark.FileCapture(input_file, display_filter=f"{filter_string}", output_file=f'{output_file}')
        capture.set_debug()
        filtered_packets = [packet for packet in capture]
        logging.debug(f'filtered_packets,{filtered_packets} - output: {output_file}, filterString:{filter_string}')

        return output_file

    @classmethod
    def update_messages_with_identifier_key(cls, df, item_id):
        try:
            with transaction.atomic():
                upload_table = UploadedFile.objects.get(id=item_id)
                logging.error(f"Started filtering messages for each call flow: {upload_table.filename}")

                # The columns to check for undesired values
                columns_to_check = [
                    'f1ap.C_RNTI',
                    'f1ap.GNB_DU_UE_F1AP_ID',
                    'f1ap.GNB_CU_UE_F1AP_ID',
                    'e1ap.GNB_CU_CP_UE_E1AP_ID',
                    'e1ap.GNB_CU_UP_UE_E1AP_ID',
                    'ngap.RAN_UE_NGAP_ID',
                    'ngap.AMF_UE_NGAP_ID',
                    'xnap.NG_RANnodeUEXnAPID_src',
                    'xnap.NG_RANnodeUEXnAPID_dst',
                ]

                # Specify undesired values
                undesired_values = ["none", "nan", "", None, "NaN", np.nan]

                # Create a mask to filter out rows with undesired values in the specified columns
                mask = df[columns_to_check].apply(
                    lambda col: ~col.astype(str).str.lower().isin(undesired_values)
                )

                filtered_df = df[mask.any(axis=1)]
                identifiers = Identifiers.objects.filter(uploaded_file_id=item_id)

                messages_to_insert = []
                bulk_update_data = []

                # Use ThreadPoolExecutor to process messages concurrently for each identifier
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = []
                    for identifier_data in identifiers:
                        logging.debug(f"Identifier data: {identifier_data.c_rnti}, id: {identifier_data.id}")
                        filter_conditions = cls.create_filter_conditions(identifier_data, filtered_df)

                        updated_messages = filter_conditions
                        future = executor.submit(cls.process_messages, identifier_data, updated_messages, messages_to_insert, bulk_update_data, item_id)
                        futures.append(future)

                        # Wait for all futures to complete
                        concurrent.futures.wait(futures, timeout=None, return_when=concurrent.futures.ALL_COMPLETED)

                batch_size = 400
                total_messages = len(messages_to_insert)
                logging.error(f"Messages filter has been completed : {total_messages}")

                logging.error(f"total_messages to insert : {total_messages}")

                for start in range(0, total_messages, batch_size):
                    end = start + batch_size
                    current_batch = messages_to_insert[start:end]

                    # Bulk insert the current batch
                    Message.objects.bulk_create(current_batch)
                logging.error(f"Messages insertion has been completed!!")

                cls.bulk_update_identifiers(bulk_update_data)

        except Exception as e:
            logging.error(f"Exception during update_messages_with_identifier_key: {e}")
            pass

    @classmethod
    def create_filter_conditions(cls, identifier_data, filtered_df):

        filter_conditions = pd.Series(False, index=filtered_df.index)
        if identifier_data.c_rnti != 'nan' and identifier_data.gnb_du_ue_f1ap_id != 'nan' and identifier_data.c_rnti != '00000':
            filter_conditions |= ((filtered_df['f1ap.C_RNTI'] == identifier_data.c_rnti) &
                                  (filtered_df['f1ap.GNB_DU_UE_F1AP_ID'] == identifier_data.gnb_du_ue_f1ap_id)
                                  & (filtered_df['frame.time'] == identifier_data.frame_time))
        if identifier_data.gnb_du_ue_f1ap_id != 'nan' and identifier_data.gnb_cu_ue_f1ap_id != 'nan':
            filter_conditions |= (
                    ((filtered_df['f1ap.GNB_CU_UE_F1AP_ID'] == identifier_data.gnb_cu_ue_f1ap_id) &
                     (filtered_df['f1ap.GNB_DU_UE_F1AP_ID'] == identifier_data.gnb_du_ue_f1ap_id))
                    & (filtered_df['frame.time'] > identifier_data.frame_time))

        if identifier_data.gnb_cu_cp_ue_e1ap_id != 'nan' and identifier_data.gnb_cu_up_ue_e1ap_id != 'nan':
            filter_conditions |= (
                    ((filtered_df['e1ap.GNB_CU_CP_UE_E1AP_ID'] == identifier_data.gnb_cu_cp_ue_e1ap_id) &
                     (filtered_df['frame.time'] > identifier_data.frame_time)) |
                    ((filtered_df['e1ap.GNB_CU_CP_UE_E1AP_ID'] == identifier_data.gnb_cu_cp_ue_e1ap_id) &
                     (filtered_df['e1ap.GNB_CU_UP_UE_E1AP_ID'] == identifier_data.gnb_cu_up_ue_e1ap_id)) &
                    (filtered_df['frame.time'] > identifier_data.frame_time))

        if identifier_data.ran_ue_ngap_id != 'nan' and identifier_data.amf_ue_ngap_id != 'nan':
            filter_conditions |= (((filtered_df['ngap.RAN_UE_NGAP_ID'] == identifier_data.ran_ue_ngap_id) &
                                   (filtered_df['frame.time'] > identifier_data.frame_time)) |
                                  ((filtered_df['ngap.RAN_UE_NGAP_ID'] == identifier_data.ran_ue_ngap_id) &
                                   (filtered_df['ngap.AMF_UE_NGAP_ID'] == identifier_data.amf_ue_ngap_id)) &
                                  (filtered_df['frame.time'] > identifier_data.frame_time))

        if identifier_data.xnap_src_ran_id != 'nan':
            filter_conditions |= (
                    (filtered_df['xnap.NG_RANnodeUEXnAPID_src'] == identifier_data.xnap_src_ran_id) &
                    (filtered_df['frame.time'] >= identifier_data.frame_time))

        if identifier_data.xnap_trgt_ran_id != 'nan':
            filter_conditions |= (
                    (filtered_df['xnap.NG_RANnodeUEXnAPID_dst'] == identifier_data.xnap_trgt_ran_id) &
                    (filtered_df['frame.time'] > identifier_data.frame_time))

        if identifier_data.gnb_cu_cp_ue_e1ap_id != 'nan' and identifier_data.gnb_cu_up_ue_e1ap_id == 'nan':
            filter_conditions |= (filtered_df[
                                      'e1ap.GNB_CU_CP_UE_E1AP_ID'] == identifier_data.gnb_cu_cp_ue_e1ap_id) \
                                 & (filtered_df['e1ap.GNB_CU_UP_UE_E1AP_ID'].isna() & (
                    filtered_df['frame.time'] > identifier_data.frame_time))

        if identifier_data.ran_ue_ngap_id != 'nan' and identifier_data.amf_ue_ngap_id == 'nan':
            filter_conditions |= ((filtered_df['ngap.RAN_UE_NGAP_ID'] == identifier_data.ran_ue_ngap_id) &
                                  filtered_df['ngap.AMF_UE_NGAP_ID'].isna() & (
                                          filtered_df['frame.time'] > identifier_data.frame_time))

        updated_messages = filtered_df[filter_conditions]
        condition = ((updated_messages['_ws.col.info'] == 'UEContextReleaseComplete') &
                     updated_messages['frame.protocols'].str.contains('ngap'))
        condition2 = ((updated_messages['_ws.col.info'] == 'BearerContextReleaseComplete') &
                      updated_messages['frame.protocols'].str.contains('e1ap'))
        if condition2.any() or condition.any():  # If the condition is met at least once
            if condition2.any():
                first_occurrence = condition2.idxmax()
                # Check UEContextReleaseComplete in next couple of rows
                next_rows = updated_messages.loc[first_occurrence + 1:first_occurrence + 2, '_ws.col.info']
                check_uecontext = (next_rows == 'UEContextReleaseComplete').any()
                if check_uecontext:
                    updated_messages = updated_messages.loc[:first_occurrence + 2].copy()
                else:
                    updated_messages = updated_messages.loc[:first_occurrence].copy()
            else:
                first_occurrence = condition.idxmax()
                updated_messages = updated_messages.loc[:first_occurrence].copy()

        updated_messages_copy = updated_messages.copy()

        return updated_messages_copy

    @classmethod
    def process_messages(cls, identifier_data, updated_messages, messages_to_insert, bulk_update_data, item_id):
        try:

            updated_messages_copy = updated_messages.copy()
            logging.debug(f"Before filtering, dimensions of updated_messages_copy: {updated_messages_copy.shape}")

            updated_messages_copy['identifiers_id'] = identifier_data.id
            updated_messages_copy['gnb_id'] = str(identifier_data.gnb_id)
            interface_patterns = ['f1ap', 'e1ap', 'ngap', 'xnap']

            updated_messages_copy['interface'] = updated_messages_copy['frame.protocols'].str.extract(
                f"({'|'.join(interface_patterns)})", flags=re.IGNORECASE)
            updated_messages_copy['_ws.col.info_lower'] = updated_messages_copy['_ws.col.info'].str.lower()
            INTERFACE_CONFIG_PD['_ws.col.info_lower'] = INTERFACE_CONFIG_PD['_ws.col.info'].str.lower()

            merged_messages = pd.merge(updated_messages_copy, INTERFACE_CONFIG_PD,
                                       left_on=['_ws.col.info_lower', 'interface'],
                                       right_on=['_ws.col.info_lower', 'interface'], how='left',
                                       suffixes=('_msg', '_config'))

            merged_messages.reset_index(drop=True, inplace=True)
            updated_messages_copy.reset_index(drop=True, inplace=True)

            updated_messages_copy['srcNode'] = merged_messages['srcNode']
            updated_messages_copy['dstNode'] = merged_messages['dstNode']

            # Handle special case for '00000'
            if identifier_data.c_rnti == "00000":
                condition1 = (updated_messages_copy['srcNode'] == "CUCP") & (
                        updated_messages_copy['dstNode'] == "Target_CUCP")
                condition2 = (updated_messages_copy['srcNode'] == "Target_CUCP") & (
                        updated_messages_copy['dstNode'] == "CUCP")

                updated_messages_copy.loc[condition1, ['srcNode', 'dstNode']] = ["src_CUCP", "CUCP"]
                updated_messages_copy.loc[condition2, ['srcNode', 'dstNode']] = ["CUCP", "src_CUCP"]

            # Drop the temporary 'interface' column added for merging
            updated_messages_copy.drop(columns=['interface'], inplace=True)
            logging.debug(f"After filtering, dimensions of updated_messages_copy: {updated_messages_copy.shape}")
            updated_messages = updated_messages_copy
            logging.debug(f"After filtering, dimensions of updated_messages: {updated_messages.shape}")
            messages_to_insert.extend(cls.create_message_instances(updated_messages, identifier_data, item_id))
            bulk_update_data.append(cls.create_bulk_update_data(updated_messages, identifier_data))

        except Exception as e:
            logging.error(f"An error occurred in process_messages: {str(e)}")

   
    @classmethod
    def create_message_instances(cls, updated_messages, identifier_data, item_id):

        def create_message(row):
            return Message(
                frame_number=row['frame.number'],
                frame_time=row['frame.time'],
                ip_src=row['ip.src'],
                ip_dst=row['ip.dst'],
                protocol=row['frame.protocols'],
                f1_proc=row['f1ap.procedureCode'],
                e1_proc=row['e1ap.procedureCode'],
                ng_proc=row['ngap.procedureCode'],
                c1_rrc=row['f1ap.pLMN_Identity'],
                c2_rrc=row['nr-rrc.ng_5G_S_TMSI_Part1'],
                mm_message_type=row['nas-5gs.mm.message_type'],
                sm_message_type=row['nas-5gs.sm.message_type'],
                message=row['_ws.col.info'],
                src_node=row["srcNode"],
                dst_node=row["dstNode"],
                message_json=None,
                c_rnti=row['f1ap.C_RNTI'],
                gnb_du_ue_f1ap_id=row['f1ap.GNB_DU_UE_F1AP_ID'],
                gnb_cu_ue_f1ap_id=row['f1ap.GNB_CU_UE_F1AP_ID'],
                gnb_cu_cp_ue_e1ap_id=row['e1ap.GNB_CU_CP_UE_E1AP_ID'],
                gnb_cu_up_ue_e1ap_id=row['e1ap.GNB_CU_UP_UE_E1AP_ID'],
                ran_ue_ngap_id=row['ngap.RAN_UE_NGAP_ID'],
                amf_ue_ngap_id=row['ngap.AMF_UE_NGAP_ID'],
                xnap_src_ran_id=row['xnap.NG_RANnodeUEXnAPID_src'],
                xnap_trgt_ran_id=row['xnap.NG_RANnodeUEXnAPID_dst'],
                uploaded_file_id=item_id,
                gnb_id=row['gnb_id'],
                identifiers_id=identifier_data.id,
                f1ap_cause=row['f1ap.cause_desc'],
                ngap_cause=row['ngap.cause_desc'],
                nas_cause=row['nas.cause_desc']
            )

        try:
            messages = updated_messages.apply(create_message, axis=1)
        except Exception as e:
            logging.error(f"An error occurred in create_message_instances: {str(e)}")

        return messages.tolist()


    @classmethod
    def create_bulk_update_data(cls, updated_messages, identifier_data):
        try:
            rrc_stats = sh.calculate_rrc_stats(updated_messages)
            initial_ctxt_stats = sh.calculate_initial_ctxt_stats(updated_messages)
            bearer_ctxt_stats = sh.calculate_bearerctxt_stats(updated_messages)
            xnap_handover_stats = sh.calculate_handover_stats(updated_messages)
            cause_code = sh.get_cause_data(updated_messages)
            bulk_update_data = {
                'id': identifier_data.id,
                **rrc_stats,
                **initial_ctxt_stats,
                **bearer_ctxt_stats,
                **xnap_handover_stats,
                **cause_code,
            }
        except Exception as e:
            logging.error(f"An error occurred in processing stats: {str(e)}")
            return None
        return bulk_update_data

    @classmethod
    def bulk_update_identifiers(cls, bulk_update_data):
        logging.error(f"Identifier update with Stats Started. {len(bulk_update_data)}")

        for data in bulk_update_data:
            identifier_id = data['id']
            Identifiers.objects.update_or_create(
                id=identifier_id,
                defaults=data,
            )
        logging.error(f"Identifier update has been completed!!")
