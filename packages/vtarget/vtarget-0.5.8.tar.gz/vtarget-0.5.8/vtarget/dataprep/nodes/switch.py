import json

import numpy as np
import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class Switch:
    def __init__(self):
        self.functionApply = ["is null", "is not null"]
        self.noValueRequired = ["is empty", "is not empty"]

    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# SWITCH")

        cases: list = settings["cases"] if "cases" in settings and settings["cases"] else []
        default_value: str = settings["default_value"] if "default_value" in settings and settings["default_value"] else None
        default_value_field: str = settings["default_value_field"] if "default_value_field" in settings and settings["default_value_field"] else None
        new_column: str = settings["new_column"] if "new_column" in settings and settings["new_column"] else "new_column"

        if not default_value and not default_value_field:
            msg = app_message.dataprep["nodes"]["switch"]["default_value"](node_key)
            return bug_handler.default_on_error(flow_id, node_key, msg)

        try:
            conditions = []
            outputs = []
            script.append("conditions = []")
            script.append("outputs = []")
            for case in cases:
                output: str = case["output"] if "output" in case and case["output"] else None
                output_field: str = case["output_field"] if "output_field" in case and case["output_field"] else None
                if not output and not output_field:
                    raise Exception("Falta el 'Valor' o 'Columna' por defecto de algún 'Case'")

                query = ""
                for condition in case["conditions"]:
                    rule = f" {condition['rule']} " if "rule" in condition else ""
                    operator = condition["operator"]
                    field = condition["field"]

                    value: str = condition["value"] if "value" in condition else None
                    value_field: str = condition["value_field"] if "value_field" in condition else None

                    if not value and not value_field:
                        msg = app_message.dataprep["nodes"]["switch"]["not_value_or_field"](node_key)
                        return bug_handler.default_on_error(flow_id, node_key, msg)

                    if value:
                        # Para los que requieren función
                        if operator in self.functionApply:
                            value = f"pd.isnull(df['{field}'])" if operator == "is null" else f"pd.notnull(df['{field}'])"
                            query += f"{rule}{value}"
                        # Para los que no requieren un valor
                        elif operator in self.noValueRequired:
                            value = f'df["{field}"] == ""' if operator == "is empty" else f'df["{field}"] != ""'
                            query += f"{rule}{value}"
                        else:
                            # Se formatean los tipos de datos
                            value = " '{}'".format(value) if pd.api.types.is_string_dtype(df[field]) else value
                            value = " '{}'".format(value) if pd.api.types.is_datetime64_any_dtype(df[field]) else value
                            query += f"{rule}df['{field}'] {operator}{value}"
                    else:
                        if value_field not in df.columns:
                            msg = app_message.dataprep["nodes"]["switch"]["not_column_in_df"](node_key)
                            return bug_handler.default_on_error(flow_id, node_key, msg)

                        query += f"{rule}df['{field}'] {operator} df['{value_field}']"

                output_new = output if output else df[output_field]
                outputs.append(output_new)
                script.append(f"outputs.append({output_new})")
                conditions.append(pd.eval(query))
                script.append(f'conditions.append(pd.eval("{query}"))')

            df[new_column] = np.select(conditions, outputs, default=default_value if default_value else df[default_value_field])

            try:
                df[new_column] = pd.to_numeric(df[new_column])
            except Exception as e:
                print(new_column, e)

            default_value_new = "'" + default_value + "'" if default_value else "df['" + default_value_field + "']"
            script.append(f'df["{new_column}"] = np.select(conditions, outputs, default={default_value_new})')

        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_on_error(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(e.args)})")

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return {"Out": df}
