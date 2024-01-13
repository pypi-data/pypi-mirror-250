import functools
import itertools
import logging

from ..types import changes, concepts


class ResponseParser:

    @functools.cached_property
    def logger(self) -> logging.Logger:
        return logging.getLogger('Response Parser')

    @staticmethod
    def parse_list_of_tables(response: list[dict]) -> list[concepts.Table]:
        return [concepts.Table(id=table['id'],
                               name=table['name'],
                               fields=[
                                   concepts.Field(
                                       id=field['id'],
                                       name=field['name'],
                                       type=field['type']
                                   ) for field in table['fields']
                               ]
                               ) for table in response]

    def parse_field_value(self, field_value: str | list | dict) -> str | list:
        if isinstance(field_value, list):
            return [self.parse_field_value(value) for value in field_value]

        if isinstance(field_value, dict):
            if 'linkedRecordIds' in field_value:
                return list(itertools.chain.from_iterable([
                    self.parse_field_value(value)
                    for value in field_value['valuesByLinkedRecordId'].values()
                ]))

            # If user field use the email as the value
            if 'email' in field_value:
                return field_value['email']

            # Drop down case take the name as the value
            if 'color' in field_value and 'name' in field_value:
                return field_value['name']

            if 'id' in field_value:
                return field_value['id']

            # If select or url field use the name as the value
            if 'name' in field_value:
                return field_value['name']

            raise NotImplementedError(f'Unknown field value: {field_value}')

        return field_value

    def parse_list_of_rows(self, table: concepts.Table, response: dict) -> list[concepts.Row]:
        fields = {field.name: field for field in table.fields}

        return [concepts.Row(
            id=row['id'],
            field_values=[concepts.FieldValue(
                field=fields[name],
                value=self.parse_field_value(value)
            ) for name, value in row['fields'].items()]
        ) for row in response['records']]

    def _parse_changed_records_by_id(self, table_id: concepts.TableId, records: dict) -> list[changes.Change]:
        out = []

        for row_id, values in records.items():
            values = values.get('current', {}).get('cellValuesByFieldId', {})

            for field_id, value in values.items():
                out.append(changes.CellChange(
                    table_id=table_id,
                    row_id=row_id,
                    field_id=field_id,
                    value=self.parse_field_value(value)
                ))

        return out

    @staticmethod
    def _parse_destroyed_filed_id(table_id: str, fields: dict) -> list[changes.Change]:
        return [changes.DestroyedField(table_id=table_id, field_id=field_id) for field_id in fields]

    @staticmethod
    def _parse_created_fields_by_id(table_id: str, fields: dict) -> list[changes.Change]:
        out = []

        for filed_id, field in fields.items():
            out.append(
                changes.NewField(
                    table_id=table_id,
                    field=concepts.Field(
                        id=filed_id,
                        name=field['name'],
                        type=field['type']
                    )
                )
            )

        return out

    def _parse_created_records_by_id(self, table_id: str, rows: dict) -> list[changes.Change]:
        created_rows = [
            changes.NewRow(table_id=table_id, row=concepts.Row(id=row_id, field_values=[]))
            for row_id in rows
        ]
        new_values = []

        for row_id, values in rows.items():
            new_values.extend(self._parse_changed_records_by_id(table_id, {row_id: {'current': values}}))

        return created_rows + new_values

    @staticmethod
    def _parse_deleted_record_ids(table_id: str, rows: list) -> list[changes.Change]:
        return [changes.DestroyedRow(table_id=table_id, row_id=row_id) for row_id in rows]

    @staticmethod
    def _parse_changed_fields_by_id(table_id: str, fields: dict) -> list[changes.Change]:
        type_changes = [
            changes.FieldTypeChange(table_id=table_id, field_id=field_id, field_type=field['current']['type'])
            for field_id, field in fields.items()
            if field['current'].get('type')
        ]

        name_changes = [
            changes.FieldNameChange(table_id=table_id, field_id=field_id, field_name=field['current']['name'])
            for field_id, field in fields.items()
            if field['current'].get('name')
        ]

        return [*type_changes, *name_changes]

    @staticmethod
    def _parse_changed_metadata(table_id: str, metadata: dict) -> list[changes.Change]:
        return [changes.TableNameChange(table_id=table_id, table_name=metadata['current']['name'])]

    def _parse_created_tables_by_id(self, table_id: str, received_changes: dict) -> list[changes.Change]:

        if 'metadata' not in received_changes:
            return [changes.ImportedTable(table_id=table_id)]

        new_table = [
            changes.NewTable(
                table=concepts.Table(
                    id=table_id,
                    name=received_changes['metadata']['name'],
                    fields=[
                        concepts.Field(id=field_id, name=field['name'], type=field['type'])
                        for field_id, field in received_changes.get('fieldsById', {}).items()
                    ]
                )
            )
        ]

        new_values = self._parse_created_records_by_id(table_id, received_changes['recordsById'])

        return new_table + new_values

    @staticmethod
    def _parse_destroyed_tables_id(table_id: str) -> list[changes.Change]:
        return [changes.DestroyedTable(table_id=table_id)]

    def _parse_table_change_by_id(self, table_id: str, received_changes: dict) -> list[changes.Change]:
        out = []

        for key, change in received_changes.items():

            if key == 'changedRecordsById':
                out.extend(self._parse_changed_records_by_id(table_id, change))

            elif key == 'destroyedFieldIds':
                out.extend(self._parse_destroyed_filed_id(table_id, change))

            elif key == 'createdFieldsById':
                out.extend(self._parse_created_fields_by_id(table_id, change))

            elif key == 'createdRecordsById':
                out.extend(self._parse_created_records_by_id(table_id, change))

            elif key == 'destroyedRecordIds':
                out.extend(self._parse_deleted_record_ids(table_id, change))

            elif key == 'changedFieldsById':
                out.extend(self._parse_changed_fields_by_id(table_id, change))

            elif key == 'changedMetadata':
                out.extend(self._parse_changed_metadata(table_id, change))

            else:
                raise ValueError(f"Unknown change type: {key}")

        return out

    def parse_webhook_payload(self, payload: dict) -> list[changes.Change]:
        out = []
        recognized_pyload_type = False

        try:

            if 'changedTablesById' in payload:
                recognized_pyload_type = True

                for table_id, received_changes in payload.get('changedTablesById', {}).items():
                    out.extend(self._parse_table_change_by_id(table_id, received_changes))

            if 'createdTablesById' in payload:
                recognized_pyload_type = True

                for table_id, received_changes in payload.get('createdTablesById', {}).items():
                    out.extend(self._parse_created_tables_by_id(table_id, received_changes))

            if 'destroyedTableIds' in payload:
                recognized_pyload_type = True

                for table_id in payload.get('destroyedTableIds', []):
                    out.extend(self._parse_destroyed_tables_id(table_id))

            if not recognized_pyload_type:
                self.logger.error('Unknown payload type')
                self.logger.error(payload)

                raise RuntimeError('Unknown payload type')

            if not out:
                self.logger.warning('Could not find any changes in payload')
                self.logger.warning(payload)

        except Exception as e:
            self.logger.error('Error parsing webhook payload')
            self.logger.error(payload)
            self.logger.exception(e)
            raise e

        return out


test = {
  'timestamp': '2023-10-24T14:26:16.151Z',
  'baseTransactionNumber': 7470,
  'actionMetadata': {
    'source': 'client',
    'sourceMetadata': {
      'user': {
        'id': 'usrrHWy4XEvLEqJ2y',
        'email': 'leo@hipgnosissongs.com',
        'permissionLevel': 'create',
        'name': 'Leo Pinnock',
        'profilePicUrl': 'https://static.airtable.com/images/userIcons/user_icon_5.png'
      }
    }
  },
  'payloadFormat': 'v0',
  'createdTablesById': {
    'tblBHR9xBwZlcR5ZR': {
      'recordsById': {
        'recuM89sUTi1sxtP1': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14318,
            'fldVSsXZiAi8GaBd3': 'T3038688147',
            'fldunLhs9CUE6wMmc': 'TA MIN VALS',
            'fldF9pDFMu9DEwflz': {
              'id': 'seleQK5Ttjoi8Op48',
              'name': 'BX11',
              'color': 'pinkLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'seltY4cNwq0kbOv9P',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY',
              'color': 'pinkLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recQuYqpdiEJ8Fu8i': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14320,
            'fldVSsXZiAi8GaBd3': 'T9090346477',
            'fldunLhs9CUE6wMmc': 'TANGOS DEL ANTONI',
            'fldF9pDFMu9DEwflz': {
              'id': 'seleQK5Ttjoi8Op48',
              'name': 'BX11',
              'color': 'pinkLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'seltY4cNwq0kbOv9P',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY',
              'color': 'pinkLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec0IsMDpbr26yOqA': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 12347,
            'fldVSsXZiAi8GaBd3': 'T0700291515',
            'fldunLhs9CUE6wMmc': 'CHIC CHEER',
            'fldF9pDFMu9DEwflz': {
              'id': 'seludkhJa87ih3Nk9',
              'name': 'CAT2',
              'color': 'grayLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selJQlnPtHx1Wsyxf',
              'name': 'CAT004 - BERNARD EDWARDS',
              'color': 'grayLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recu5Neqo4IBNLJnY': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 12085,
            'fldVSsXZiAi8GaBd3': 'T9117067648',
            'fldunLhs9CUE6wMmc': 'AKEEM SEES ROSE PETALS',
            'fldF9pDFMu9DEwflz': {
              'id': 'selz6TjwRZo2k4pvo',
              'name': 'BX01',
              'color': 'tealLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selSUAluKjI7GMXoN',
              'name': 'BX004 - NILE RODGERS - SONY PURCHASE',
              'color': 'tealLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'reco2o0j93dPqDYAo': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 12151,
            'fldVSsXZiAi8GaBd3': None,
            'fldunLhs9CUE6wMmc': 'AXEL CHANGES MATRIX',
            'fldF9pDFMu9DEwflz': {
              'id': 'selfFKJTUxLS6Gnms',
              'name': 'BX04',
              'color': 'cyanLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selrNhHlGS2xfFrDK',
              'name': 'BX004 - NILE RODGERS - TBC',
              'color': 'cyanLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recIeQgyMpysDgcJ1': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 12152,
            'fldVSsXZiAi8GaBd3': None,
            'fldunLhs9CUE6wMmc': 'AXEL ELLIS AND DAVE',
            'fldF9pDFMu9DEwflz': {
              'id': 'selfFKJTUxLS6Gnms',
              'name': 'BX04',
              'color': 'cyanLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selrNhHlGS2xfFrDK',
              'name': 'BX004 - NILE RODGERS - TBC',
              'color': 'cyanLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recU88ui82WFSiukS': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 12153,
            'fldVSsXZiAi8GaBd3': None,
            'fldunLhs9CUE6wMmc': 'AXEL FOX',
            'fldF9pDFMu9DEwflz': {
              'id': 'selfFKJTUxLS6Gnms',
              'name': 'BX04',
              'color': 'cyanLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selrNhHlGS2xfFrDK',
              'name': 'BX004 - NILE RODGERS - TBC',
              'color': 'cyanLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recKYE1uVVo5mfCvS': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 12154,
            'fldVSsXZiAi8GaBd3': None,
            'fldunLhs9CUE6wMmc': 'AXEL IN MIRROR',
            'fldF9pDFMu9DEwflz': {
              'id': 'selfFKJTUxLS6Gnms',
              'name': 'BX04',
              'color': 'cyanLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selrNhHlGS2xfFrDK',
              'name': 'BX004 - NILE RODGERS - TBC',
              'color': 'cyanLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recGnUXSgQlkWWeLx': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 12155,
            'fldVSsXZiAi8GaBd3': None,
            'fldunLhs9CUE6wMmc': 'AXEL SAVES THE KIDS',
            'fldF9pDFMu9DEwflz': {
              'id': 'selfFKJTUxLS6Gnms',
              'name': 'BX04',
              'color': 'cyanLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selrNhHlGS2xfFrDK',
              'name': 'BX004 - NILE RODGERS - TBC',
              'color': 'cyanLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec7FbaPrTfMFYujP': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 12347,
            'fldVSsXZiAi8GaBd3': 'T0700291515',
            'fldunLhs9CUE6wMmc': 'CHIC CHEER',
            'fldF9pDFMu9DEwflz': {
              'id': 'selz6TjwRZo2k4pvo',
              'name': 'BX01',
              'color': 'tealLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selSUAluKjI7GMXoN',
              'name': 'BX004 - NILE RODGERS - SONY PURCHASE',
              'color': 'tealLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recfzHW0fqk2q5mJz': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14648,
            'fldVSsXZiAi8GaBd3': 'T9141262342',
            'fldunLhs9CUE6wMmc': 'BETTER DAYS',
            'fldF9pDFMu9DEwflz': {
              'id': 'selOpdZcYuOsL5Ons',
              'name': 'CAT3',
              'color': 'blueLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selOMBjDTYBE64jpG',
              'name': 'CAT051 - Tom Delonge - Sony/EMI Works',
              'color': 'blueLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'reclNKkInqwFy4dMm': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14649,
            'fldVSsXZiAi8GaBd3': 'T9105240322',
            'fldunLhs9CUE6wMmc': 'BOXING DAY',
            'fldF9pDFMu9DEwflz': {
              'id': 'selOpdZcYuOsL5Ons',
              'name': 'CAT3',
              'color': 'blueLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selOMBjDTYBE64jpG',
              'name': 'CAT051 - Tom Delonge - Sony/EMI Works',
              'color': 'blueLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recbRIl2Rr9NgS4Bv': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14650,
            'fldVSsXZiAi8GaBd3': 'T9200446599',
            'fldunLhs9CUE6wMmc': 'DISASTER',
            'fldF9pDFMu9DEwflz': {
              'id': 'selOpdZcYuOsL5Ons',
              'name': 'CAT3',
              'color': 'blueLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selOMBjDTYBE64jpG',
              'name': 'CAT051 - Tom Delonge - Sony/EMI Works',
              'color': 'blueLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recY1E7ECxkeAfAgH': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14651,
            'fldVSsXZiAi8GaBd3': 'T9149729395',
            'fldunLhs9CUE6wMmc': 'DOGS EATING DOGS',
            'fldF9pDFMu9DEwflz': {
              'id': 'selOpdZcYuOsL5Ons',
              'name': 'CAT3',
              'color': 'blueLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selOMBjDTYBE64jpG',
              'name': 'CAT051 - Tom Delonge - Sony/EMI Works',
              'color': 'blueLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recQkRCGacPSZsCif': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14652,
            'fldVSsXZiAi8GaBd3': 'T9104960192',
            'fldunLhs9CUE6wMmc': 'PRETTY LITTLE GIRL',
            'fldF9pDFMu9DEwflz': {
              'id': 'selOpdZcYuOsL5Ons',
              'name': 'CAT3',
              'color': 'blueLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selOMBjDTYBE64jpG',
              'name': 'CAT051 - Tom Delonge - Sony/EMI Works',
              'color': 'blueLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rectLwN6OCbdIFmvk': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14653,
            'fldVSsXZiAi8GaBd3': 'T9149729351',
            'fldunLhs9CUE6wMmc': 'WHEN I WAS YOUNG',
            'fldF9pDFMu9DEwflz': {
              'id': 'selOpdZcYuOsL5Ons',
              'name': 'CAT3',
              'color': 'blueLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selOMBjDTYBE64jpG',
              'name': 'CAT051 - Tom Delonge - Sony/EMI Works',
              'color': 'blueLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recmKxDNEWydx0OaY': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14654,
            'fldVSsXZiAi8GaBd3': 'T9141310272',
            'fldunLhs9CUE6wMmc': 'WRECKED HIM',
            'fldF9pDFMu9DEwflz': {
              'id': 'selOpdZcYuOsL5Ons',
              'name': 'CAT3',
              'color': 'blueLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selOMBjDTYBE64jpG',
              'name': 'CAT051 - Tom Delonge - Sony/EMI Works',
              'color': 'blueLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recypCHgkkJLI1Wjz': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14655,
            'fldVSsXZiAi8GaBd3': 'T9149728574',
            'fldunLhs9CUE6wMmc': 'ZULU',
            'fldF9pDFMu9DEwflz': {
              'id': 'selOpdZcYuOsL5Ons',
              'name': 'CAT3',
              'color': 'blueLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selOMBjDTYBE64jpG',
              'name': 'CAT051 - Tom Delonge - Sony/EMI Works',
              'color': 'blueLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recCoDna1BMb2J4Xn': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14656,
            'fldVSsXZiAi8GaBd3': 'T9063262920',
            'fldunLhs9CUE6wMmc': 'THE FALLEN INTERLUDE',
            'fldF9pDFMu9DEwflz': {
              'id': 'selQ7OtktvBAu902S',
              'name': 'TOM1',
              'color': 'cyanLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selC2mcgjw9IVBv4s',
              'name': 'CAT051 - Tom Delonge - UMPG Works',
              'color': 'cyanLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec28QoWNJSbhg1S3': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14657,
            'fldVSsXZiAi8GaBd3': 'T9289169795',
            'fldunLhs9CUE6wMmc': "WHAT'S MY AGE AGAIN? / A MILLI",
            'fldF9pDFMu9DEwflz': {
              'id': 'selOpdZcYuOsL5Ons',
              'name': 'CAT3',
              'color': 'blueLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selOMBjDTYBE64jpG',
              'name': 'CAT051 - Tom Delonge - Sony/EMI Works',
              'color': 'blueLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec7MgimuZJ9n0EtD': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14658,
            'fldVSsXZiAi8GaBd3': 'T3045040511',
            'fldunLhs9CUE6wMmc': 'CHE CAZZO RIDI',
            'fldF9pDFMu9DEwflz': {
              'id': 'selOpdZcYuOsL5Ons',
              'name': 'CAT3',
              'color': 'blueLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selOMBjDTYBE64jpG',
              'name': 'CAT051 - Tom Delonge - Sony/EMI Works',
              'color': 'blueLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recnjni5l9QE0oEmj': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14659,
            'fldVSsXZiAi8GaBd3': 'T3021125026',
            'fldunLhs9CUE6wMmc': 'FUCK YOU GOODBYE',
            'fldF9pDFMu9DEwflz': {
              'id': 'selOpdZcYuOsL5Ons',
              'name': 'CAT3',
              'color': 'blueLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selOMBjDTYBE64jpG',
              'name': 'CAT051 - Tom Delonge - Sony/EMI Works',
              'color': 'blueLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec8nkjnDrOjfOan4': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14995,
            'fldVSsXZiAi8GaBd3': 'T0708971894',
            'fldunLhs9CUE6wMmc': 'HERETIC',
            'fldF9pDFMu9DEwflz': {
              'id': 'selzjIRsPbohyKvtf',
              'name': 'CHR2',
              'color': 'tealLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selqOHxivr4cq8IDa',
              'name': 'Chris Cornell - You Make Me Sick I Make Music (BMG Agmt)',
              'color': 'tealLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recrCWjzMPuDy7GsJ': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14995,
            'fldVSsXZiAi8GaBd3': 'T0708971894',
            'fldunLhs9CUE6wMmc': 'HERETIC',
            'fldF9pDFMu9DEwflz': {
              'id': 'sel0TyPmolOiNA2aK',
              'name': 'CHR3',
              'color': 'greenLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selylrjRxmtobolZg',
              'name': 'Chris Cornell - Loud Love Partnership Dispute',
              'color': 'greenLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec5ulDNRsDUPPIPz': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14996,
            'fldVSsXZiAi8GaBd3': None,
            'fldunLhs9CUE6wMmc': 'I AWAKE',
            'fldF9pDFMu9DEwflz': {
              'id': 'selNjcyk0j2iOhahX',
              'name': 'CHR1',
              'color': 'yellowLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selCzV0gLK7n3LX1l',
              'name': 'Chris Cornell - Silver Income Participation',
              'color': 'yellowLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recefTRpQZRnCQLPw': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14996,
            'fldVSsXZiAi8GaBd3': None,
            'fldunLhs9CUE6wMmc': 'I AWAKE',
            'fldF9pDFMu9DEwflz': {
              'id': 'selzjIRsPbohyKvtf',
              'name': 'CHR2',
              'color': 'tealLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selqOHxivr4cq8IDa',
              'name': 'Chris Cornell - You Make Me Sick I Make Music (BMG Agmt)',
              'color': 'tealLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recDjS8B2K7VrvX3q': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14996,
            'fldVSsXZiAi8GaBd3': None,
            'fldunLhs9CUE6wMmc': 'I AWAKE',
            'fldF9pDFMu9DEwflz': {
              'id': 'sel0TyPmolOiNA2aK',
              'name': 'CHR3',
              'color': 'greenLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selylrjRxmtobolZg',
              'name': 'Chris Cornell - Loud Love Partnership Dispute',
              'color': 'greenLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recxwpPIoszbxb9m5': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 15551,
            'fldVSsXZiAi8GaBd3': 'T9001124512',
            'fldunLhs9CUE6wMmc': 'FARMER IN THE DELL',
            'fldF9pDFMu9DEwflz': {
              'id': 'seleQK5Ttjoi8Op48',
              'name': 'BX11',
              'color': 'pinkLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'seltY4cNwq0kbOv9P',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY',
              'color': 'pinkLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec7bxO4p8CySyF4Q': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14646,
            'fldVSsXZiAi8GaBd3': 'T3116860125',
            'fldunLhs9CUE6wMmc': 'LIE TO ME (FEAT. JULIA MICHAELS)',
            'fldF9pDFMu9DEwflz': {
              'id': 'seliiPGGM8cLY95hy',
              'name': 'CA21',
              'color': 'orangeLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'seldA7gd6VOHqZID2',
              'name': 'CAT085 - Andrew Watt',
              'color': 'orangeLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recXqur3zIAg6c9Re': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14656,
            'fldVSsXZiAi8GaBd3': 'T9063262920',
            'fldunLhs9CUE6wMmc': 'THE FALLEN INTERLUDE',
            'fldF9pDFMu9DEwflz': {
              'id': 'seljkqvIvHfrY1NeY',
              'name': 'CA23',
              'color': 'redLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selcXFNDFI9un4OKS',
              'name': 'CAT051 - Tom Delonge - VWE Partnership Songs',
              'color': 'redLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recnpPK38qVZPJQil': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 15674,
            'fldVSsXZiAi8GaBd3': 'T9306427952',
            'fldunLhs9CUE6wMmc': 'VOICES',
            'fldF9pDFMu9DEwflz': {
              'id': 'seljkqvIvHfrY1NeY',
              'name': 'CA23',
              'color': 'redLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selcXFNDFI9un4OKS',
              'name': 'CAT051 - Tom Delonge - VWE Partnership Songs',
              'color': 'redLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'reclUr64xp8H6hEkX': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 15674,
            'fldVSsXZiAi8GaBd3': 'T9306427952',
            'fldunLhs9CUE6wMmc': 'VOICES',
            'fldF9pDFMu9DEwflz': {
              'id': 'selQ7OtktvBAu902S',
              'name': 'TOM1',
              'color': 'cyanLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selC2mcgjw9IVBv4s',
              'name': 'CAT051 - Tom Delonge - UMPG Works',
              'color': 'cyanLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recWShN9Md5vza58J': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 15673,
            'fldVSsXZiAi8GaBd3': 'T3054874743',
            'fldunLhs9CUE6wMmc': 'WASTED YEAR',
            'fldF9pDFMu9DEwflz': {
              'id': 'seljkqvIvHfrY1NeY',
              'name': 'CA23',
              'color': 'redLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selcXFNDFI9un4OKS',
              'name': 'CAT051 - Tom Delonge - VWE Partnership Songs',
              'color': 'redLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recnbX1LLjKHPXcQW': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 15673,
            'fldVSsXZiAi8GaBd3': 'T3054874743',
            'fldunLhs9CUE6wMmc': 'WASTED YEAR',
            'fldF9pDFMu9DEwflz': {
              'id': 'selQ7OtktvBAu902S',
              'name': 'TOM1',
              'color': 'cyanLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selC2mcgjw9IVBv4s',
              'name': 'CAT051 - Tom Delonge - UMPG Works',
              'color': 'cyanLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recIgCL2TlEMX2O0J': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 15693,
            'fldVSsXZiAi8GaBd3': 'T3103105546',
            'fldunLhs9CUE6wMmc': 'IT WAS FUN WHILE IT LASTED',
            'fldF9pDFMu9DEwflz': {
              'id': 'selOpdZcYuOsL5Ons',
              'name': 'CAT3',
              'color': 'blueLight1'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selOMBjDTYBE64jpG',
              'name': 'CAT051 - Tom Delonge - Sony/EMI Works',
              'color': 'blueLight1'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recVR288cDjsjbVBl': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14081,
            'fldVSsXZiAi8GaBd3': 'T0715211167',
            'fldunLhs9CUE6wMmc': 'MASTER SONG',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recxrLY0ODZljkxvF': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14082,
            'fldVSsXZiAi8GaBd3': 'T0705229453',
            'fldunLhs9CUE6wMmc': 'MIDDLE OF THE NIGHT',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recepGLXCTqXXlxjt': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14083,
            'fldVSsXZiAi8GaBd3': 'T0715211349',
            'fldunLhs9CUE6wMmc': 'MINUTE PROLOGUE',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recowtlhpPnOhCBbE': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14084,
            'fldVSsXZiAi8GaBd3': 'T0715160578',
            'fldunLhs9CUE6wMmc': 'ONE OF US CANNOT BE WRONG',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec31UkRgtQO8dloq': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14085,
            'fldVSsXZiAi8GaBd3': 'T9104886557',
            'fldunLhs9CUE6wMmc': "PLEASE DON'T PASS ME BY (A DISGRACE)",
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recxETZ5jZBZLSwiw': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14086,
            'fldVSsXZiAi8GaBd3': 'T0708487642',
            'fldunLhs9CUE6wMmc': 'PRIESTS',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'reckYV3XJnUMAjk2s': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14087,
            'fldVSsXZiAi8GaBd3': 'T0715160603',
            'fldunLhs9CUE6wMmc': 'QUEEN VICTORIA',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recgdBeA1xlU10UiH': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14088,
            'fldVSsXZiAi8GaBd3': 'T0715209407',
            'fldunLhs9CUE6wMmc': 'SEEMS SO LONG AGO, NANCY',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recZFCQpXEiqSYSFh': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14089,
            'fldVSsXZiAi8GaBd3': 'T0708488076',
            'fldunLhs9CUE6wMmc': 'SING ANOTHER SONG, BOYS',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rech8SxJPhU3n0faL': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14090,
            'fldVSsXZiAi8GaBd3': 'T9104886591',
            'fldunLhs9CUE6wMmc': 'SISTERS OF MERCY',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recWAWLOHKFKjXySR': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14091,
            'fldVSsXZiAi8GaBd3': 'T0715141711',
            'fldunLhs9CUE6wMmc': 'SO LONG MARIANNE',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec7zh1PxXkUMqaMs': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14092,
            'fldVSsXZiAi8GaBd3': 'T0705230029',
            'fldunLhs9CUE6wMmc': 'SPLINTER',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec8kybpaYwzqczqz': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14093,
            'fldVSsXZiAi8GaBd3': 'T0705227195',
            'fldunLhs9CUE6wMmc': 'STORE ROOM',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recGs75gte1NOHi1g': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14095,
            'fldVSsXZiAi8GaBd3': 'T0715160636',
            'fldunLhs9CUE6wMmc': 'STORIES OF THE STREET',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recV7pAhK3uIKJsg2': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14096,
            'fldVSsXZiAi8GaBd3': 'T0715214359',
            'fldunLhs9CUE6wMmc': 'STORY OF ISAAC',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recQgVLkSdWOqNUXu': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14097,
            'fldVSsXZiAi8GaBd3': 'T0715141733',
            'fldunLhs9CUE6wMmc': 'TAKE THIS LONGING',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recAE7V8B4URtHVPD': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14098,
            'fldVSsXZiAi8GaBd3': 'T0715130383',
            'fldunLhs9CUE6wMmc': 'TEACHERS',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recXDSlzCAuHFlrnC': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14099,
            'fldVSsXZiAi8GaBd3': 'T0710295310',
            'fldunLhs9CUE6wMmc': 'THE BUTCHER',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recCsuRFb95nlEkpC': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14100,
            'fldVSsXZiAi8GaBd3': 'T0710382947',
            'fldunLhs9CUE6wMmc': 'THE OLD REVOLUTION',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recV8raNxItNaPXcW': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14101,
            'fldVSsXZiAi8GaBd3': 'T0715214780',
            'fldunLhs9CUE6wMmc': 'THERE IS A WAR',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recBhcDn9ryTbYrHu': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14102,
            'fldVSsXZiAi8GaBd3': 'T9169413063',
            'fldunLhs9CUE6wMmc': 'TONIGHT WILL BE FINE',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recgUSwy9tlCAJQKa': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14103,
            'fldVSsXZiAi8GaBd3': 'T0715141744',
            'fldunLhs9CUE6wMmc': 'WHO BY FIRE',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recOrBMa5PuZEZlVu': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14104,
            'fldVSsXZiAi8GaBd3': 'T0715162358',
            'fldunLhs9CUE6wMmc': "WHY DON'T YOU TRY",
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec5bePMeXIfsZizw': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14105,
            'fldVSsXZiAi8GaBd3': 'T0715216026',
            'fldunLhs9CUE6wMmc': 'WINTER LADY',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recHaKrcUth1kuhCF': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14106,
            'fldVSsXZiAi8GaBd3': 'T0705230289',
            'fldunLhs9CUE6wMmc': 'WORKS OF CHARITY',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recmbwxqwwztJdAUJ': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14107,
            'fldVSsXZiAi8GaBd3': 'T0715216219',
            'fldunLhs9CUE6wMmc': 'YOU KNOW WHO I AM',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recskP6OOkPwCE5Uk': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14108,
            'fldVSsXZiAi8GaBd3': 'T0702345398',
            'fldunLhs9CUE6wMmc': 'BIRD ON THE WIRE',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recmOfjnXNNuFAN06': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14109,
            'fldVSsXZiAi8GaBd3': 'T0715204811',
            'fldunLhs9CUE6wMmc': 'AVALANCHE',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recXq2tk9rYV0anpp': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14110,
            'fldVSsXZiAi8GaBd3': 'T9058593241',
            'fldunLhs9CUE6wMmc': 'AVALANCHE (TERMINAL VELOCITY)',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recuUcLxCMZBPhxEe': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14111,
            'fldVSsXZiAi8GaBd3': 'T0714710061',
            'fldunLhs9CUE6wMmc': 'BELLS',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recmGrvCd8VsoDKRP': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14112,
            'fldVSsXZiAi8GaBd3': 'T0705223386',
            'fldunLhs9CUE6wMmc': 'BLESSED IS THE MEMORY',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recP5flb6knkARhZX': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14113,
            'fldVSsXZiAi8GaBd3': 'T9169412800',
            'fldunLhs9CUE6wMmc': 'CHELSEA HOTEL NO. 2',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recZLpKNISLcMTApv': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14115,
            'fldVSsXZiAi8GaBd3': 'T0715206599',
            'fldunLhs9CUE6wMmc': 'DIAMONDS IN THE MINE',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recsvcdtVfzGxK9zW': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14116,
            'fldVSsXZiAi8GaBd3': 'T0715144298',
            'fldunLhs9CUE6wMmc': 'FAMOUS BLUE RAINCOAT',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recO6k4pYezYU0w1n': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14118,
            'fldVSsXZiAi8GaBd3': 'T9053804209',
            'fldunLhs9CUE6wMmc': 'GO BY THE BROOKS',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recGdmeuD3BCxBoqV': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14120,
            'fldVSsXZiAi8GaBd3': 'T0715144356',
            'fldunLhs9CUE6wMmc': "HEY THAT'S NO WAY TO SAY GOODBYE",
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recR47ixWkH9zrPP6': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14121,
            'fldVSsXZiAi8GaBd3': 'T9132368731',
            'fldunLhs9CUE6wMmc': 'I TRIED TO LEAVE YOU',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recVBZu90JEoqtQ1f': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14122,
            'fldVSsXZiAi8GaBd3': 'T0715209189',
            'fldunLhs9CUE6wMmc': 'IMPROVISATION',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rectz64vFB9wJdBFl': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14123,
            'fldVSsXZiAi8GaBd3': 'T0715209327',
            'fldunLhs9CUE6wMmc': 'IS THIS WHAT YOU WANTED',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recexxWdo2bUJhDTV': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14124,
            'fldVSsXZiAi8GaBd3': 'T0715138865',
            'fldunLhs9CUE6wMmc': 'JOAN OF ARC',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recd8omWyA8uFJ2Py': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14125,
            'fldVSsXZiAi8GaBd3': 'T9169412979',
            'fldunLhs9CUE6wMmc': 'LADY MIDNIGHT',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recH3wZxNFQvAJLBH': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14126,
            'fldVSsXZiAi8GaBd3': 'T9104886831',
            'fldunLhs9CUE6wMmc': "LAST YEAR'S MAN",
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recBUidv7HuBHYdyr': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14127,
            'fldVSsXZiAi8GaBd3': 'T0715210584',
            'fldunLhs9CUE6wMmc': 'LEAVING GREENSLEEVES',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'reclAIN8dyDTozeLx': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14129,
            'fldVSsXZiAi8GaBd3': None,
            'fldunLhs9CUE6wMmc': 'LOOK ON BACK',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recUAIQWdOpxGq5UZ': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14130,
            'fldVSsXZiAi8GaBd3': 'T0715210937',
            'fldunLhs9CUE6wMmc': 'LOVE CALLS YOU BY YOUR NAME',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recDUCmboGMUo6LFj': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14132,
            'fldVSsXZiAi8GaBd3': 'T0703555285',
            'fldunLhs9CUE6wMmc': 'LOVE IS THE ITEM',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recydXELCWnL787xH': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14133,
            'fldVSsXZiAi8GaBd3': 'T0715162278',
            'fldunLhs9CUE6wMmc': 'LOVER LOVER LOVER',
            'fldF9pDFMu9DEwflz': {
              'id': 'selgRQjR6iCBxQTnO',
              'name': 'BX09',
              'color': 'redLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'sell3jvNF0aU93bbb',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY/BMG',
              'color': 'redLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec9mIntCrJKh37OE': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14381,
            'fldVSsXZiAi8GaBd3': 'T0714766230',
            'fldunLhs9CUE6wMmc': 'SLOWLY I MARRIED HER',
            'fldF9pDFMu9DEwflz': {
              'id': 'seleQK5Ttjoi8Op48',
              'name': 'BX11',
              'color': 'pinkLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'seltY4cNwq0kbOv9P',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY',
              'color': 'pinkLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec2HeIIpbR7xEdbW': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14382,
            'fldVSsXZiAi8GaBd3': 'T3166998154',
            'fldunLhs9CUE6wMmc': 'DU HAR ELSKET NOK',
            'fldF9pDFMu9DEwflz': {
              'id': 'seleQK5Ttjoi8Op48',
              'name': 'BX11',
              'color': 'pinkLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'seltY4cNwq0kbOv9P',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY',
              'color': 'pinkLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recy6GeZhniLuntHi': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14384,
            'fldVSsXZiAi8GaBd3': 'T3042186307',
            'fldunLhs9CUE6wMmc': 'ESPERANT EL MIRACLE',
            'fldF9pDFMu9DEwflz': {
              'id': 'seleQK5Ttjoi8Op48',
              'name': 'BX11',
              'color': 'pinkLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'seltY4cNwq0kbOv9P',
              'name': 'BX003 - LEONARD COHEN - STRANGER MUSIC - SONY',
              'color': 'pinkLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec1rTjBjVRaDbGrb': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14409,
            'fldVSsXZiAi8GaBd3': 'T9305312849',
            'fldunLhs9CUE6wMmc': 'PUPPETS',
            'fldF9pDFMu9DEwflz': {
              'id': 'sel5k40Q700sPt59A',
              'name': 'BX10',
              'color': 'purpleLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selNsCRuvu8l5Nakq',
              'name': 'BX003 - LEONARD COHEN - OLD IDEAS - SONY ADMIN',
              'color': 'purpleLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recoscrswJw65K8vP': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14410,
            'fldVSsXZiAi8GaBd3': 'T9155145305',
            'fldunLhs9CUE6wMmc': 'SAMSON IN NEW ORLEANS',
            'fldF9pDFMu9DEwflz': {
              'id': 'sel5k40Q700sPt59A',
              'name': 'BX10',
              'color': 'purpleLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selNsCRuvu8l5Nakq',
              'name': 'BX003 - LEONARD COHEN - OLD IDEAS - SONY ADMIN',
              'color': 'purpleLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec2fNQIq6rHYdG5T': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14412,
            'fldVSsXZiAi8GaBd3': 'T9198209062',
            'fldunLhs9CUE6wMmc': 'SEEMED THE BETTER WAY',
            'fldF9pDFMu9DEwflz': {
              'id': 'sel5k40Q700sPt59A',
              'name': 'BX10',
              'color': 'purpleLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selNsCRuvu8l5Nakq',
              'name': 'BX003 - LEONARD COHEN - OLD IDEAS - SONY ADMIN',
              'color': 'purpleLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recoHdurrKyyA3kSm': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14414,
            'fldVSsXZiAi8GaBd3': 'T9120490326',
            'fldunLhs9CUE6wMmc': 'SHOW ME THE PLACE',
            'fldF9pDFMu9DEwflz': {
              'id': 'sel5k40Q700sPt59A',
              'name': 'BX10',
              'color': 'purpleLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selNsCRuvu8l5Nakq',
              'name': 'BX003 - LEONARD COHEN - OLD IDEAS - SONY ADMIN',
              'color': 'purpleLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recyx0Vk7b3yke3ZK': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14415,
            'fldVSsXZiAi8GaBd3': 'T9155145316',
            'fldunLhs9CUE6wMmc': 'SLOW',
            'fldF9pDFMu9DEwflz': {
              'id': 'sel5k40Q700sPt59A',
              'name': 'BX10',
              'color': 'purpleLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selNsCRuvu8l5Nakq',
              'name': 'BX003 - LEONARD COHEN - OLD IDEAS - SONY ADMIN',
              'color': 'purpleLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec0ZtdPH2Kp43VpZ': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14416,
            'fldVSsXZiAi8GaBd3': 'T9188480913',
            'fldunLhs9CUE6wMmc': 'STAGES',
            'fldF9pDFMu9DEwflz': {
              'id': 'sel5k40Q700sPt59A',
              'name': 'BX10',
              'color': 'purpleLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selNsCRuvu8l5Nakq',
              'name': 'BX003 - LEONARD COHEN - OLD IDEAS - SONY ADMIN',
              'color': 'purpleLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec43AMebgY0TUbxD': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14418,
            'fldVSsXZiAi8GaBd3': 'T9198051900',
            'fldunLhs9CUE6wMmc': 'STEER YOUR WAY',
            'fldF9pDFMu9DEwflz': {
              'id': 'sel5k40Q700sPt59A',
              'name': 'BX10',
              'color': 'purpleLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selNsCRuvu8l5Nakq',
              'name': 'BX003 - LEONARD COHEN - OLD IDEAS - SONY ADMIN',
              'color': 'purpleLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'reciyTsMkVPlgerok': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14421,
            'fldVSsXZiAi8GaBd3': 'T9198051933',
            'fldunLhs9CUE6wMmc': 'STRING REPRISE/TREATY',
            'fldF9pDFMu9DEwflz': {
              'id': 'sel5k40Q700sPt59A',
              'name': 'BX10',
              'color': 'purpleLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selNsCRuvu8l5Nakq',
              'name': 'BX003 - LEONARD COHEN - OLD IDEAS - SONY ADMIN',
              'color': 'purpleLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recsuGAgM4dtAKAiR': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14422,
            'fldVSsXZiAi8GaBd3': 'T0732078022',
            'fldunLhs9CUE6wMmc': 'THANKS FOR THE DANCE',
            'fldF9pDFMu9DEwflz': {
              'id': 'sel5k40Q700sPt59A',
              'name': 'BX10',
              'color': 'purpleLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selNsCRuvu8l5Nakq',
              'name': 'BX003 - LEONARD COHEN - OLD IDEAS - SONY ADMIN',
              'color': 'purpleLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'reclkYBxAFdNUzLlf': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14423,
            'fldVSsXZiAi8GaBd3': 'T9012573772',
            'fldunLhs9CUE6wMmc': 'THE FAITH',
            'fldF9pDFMu9DEwflz': {
              'id': 'sel5k40Q700sPt59A',
              'name': 'BX10',
              'color': 'purpleLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selNsCRuvu8l5Nakq',
              'name': 'BX003 - LEONARD COHEN - OLD IDEAS - SONY ADMIN',
              'color': 'purpleLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recKslw1uTYXpE7Wy': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14425,
            'fldVSsXZiAi8GaBd3': 'T9305312827',
            'fldunLhs9CUE6wMmc': 'THE GOAL',
            'fldF9pDFMu9DEwflz': {
              'id': 'sel5k40Q700sPt59A',
              'name': 'BX10',
              'color': 'purpleLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selNsCRuvu8l5Nakq',
              'name': 'BX003 - LEONARD COHEN - OLD IDEAS - SONY ADMIN',
              'color': 'purpleLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recrY2YkKZ1xuCdwp': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14426,
            'fldVSsXZiAi8GaBd3': 'T0732077972',
            'fldunLhs9CUE6wMmc': 'THE GOLDEN GATE',
            'fldF9pDFMu9DEwflz': {
              'id': 'sel5k40Q700sPt59A',
              'name': 'BX10',
              'color': 'purpleLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selNsCRuvu8l5Nakq',
              'name': 'BX003 - LEONARD COHEN - OLD IDEAS - SONY ADMIN',
              'color': 'purpleLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'rec29xJU3oGan9QPc': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14427,
            'fldVSsXZiAi8GaBd3': 'T9305312667',
            'fldunLhs9CUE6wMmc': 'THE HILLS',
            'fldF9pDFMu9DEwflz': {
              'id': 'sel5k40Q700sPt59A',
              'name': 'BX10',
              'color': 'purpleLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selNsCRuvu8l5Nakq',
              'name': 'BX003 - LEONARD COHEN - OLD IDEAS - SONY ADMIN',
              'color': 'purpleLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'reccaov2MNUSX0uCm': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14430,
            'fldVSsXZiAi8GaBd3': 'T0732078000',
            'fldunLhs9CUE6wMmc': 'THE MIST',
            'fldF9pDFMu9DEwflz': {
              'id': 'sel5k40Q700sPt59A',
              'name': 'BX10',
              'color': 'purpleLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selNsCRuvu8l5Nakq',
              'name': 'BX003 - LEONARD COHEN - OLD IDEAS - SONY ADMIN',
              'color': 'purpleLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        },
        'recIYA2x6aMrQzMau': {
          'createdTime': '2023-10-24T14:26:15.000Z',
          'cellValuesByFieldId': {
            'fldsDvqodCgmS4Y6j': 14431,
            'fldVSsXZiAi8GaBd3': 'T9305312770',
            'fldunLhs9CUE6wMmc': 'THE NIGHT OF SANTIAGO',
            'fldF9pDFMu9DEwflz': {
              'id': 'sel5k40Q700sPt59A',
              'name': 'BX10',
              'color': 'purpleLight2'
            },
            'fldOIbdz9toOMTuTd': {
              'id': 'selNsCRuvu8l5Nakq',
              'name': 'BX003 - LEONARD COHEN - OLD IDEAS - SONY ADMIN',
              'color': 'purpleLight2'
            },
            'fldUWIW1JjWe286L3': 4
          }
        }
      }
    }
  }
}


for x in ResponseParser().parse_webhook_payload(test):
    print(x)