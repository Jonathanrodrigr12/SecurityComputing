# encoding: utf-8
from project.configuration_manager import ConfigurationManger
from project.resources.utils.generals_utils import GeneralsUtils


class EntityUtils():

    @staticmethod
    def get_editables_values(entity_name, values, translate=False):
        if not isinstance(values, dict):
            return Exception

        entity_definitions = EntityUtils.get_entity_definitions(entity_name)
        result = values

        if not "editables" in entity_definitions and translate:
            try:
                result = EntityUtils.translate_dictionary(
                    entity_definitions=entity_definitions,
                    entity_properties=result)

            except Exception as error:
                raise Exception("", error)

        elif "editables" in entity_definitions:
            result = {}

            for editable in entity_definitions["editables"]:
                key = editable
                if translate:
                    key = EntityUtils.\
                        translate_attribute_name(
                            entity_definitions=entity_definitions,
                            property_name=key
                        )
                result[key] = values[editable]

        return result

    @staticmethod
    def get_entity_definitions(entity_name):
        entity_definition = GeneralsUtils.\
            get_global_data("entity_definition_" + entity_name)

        if entity_definition is not None:
            return entity_definition

        entities_definitions = GeneralsUtils.\
            get_global_data("entities_definitions")

        if entities_definitions is None:
            entities_definitions_path = ConfigurationManger.get_config(
                "ENTITIES_DEFINITIONS_PATH")

            entities_definitions = GeneralsUtils.\
                read_file(entities_definitions_path)

            GeneralsUtils.set_global_data("entities_definitions",
                                          entities_definitions)

        if entity_name not in entities_definitions:
            raise Exception("Entity name not found in entities definitions")

        return entities_definitions[entity_name]

    @staticmethod
    def get_validation_schema(schema_name):
        validation_shemes_path = ConfigurationManger.get_config(
            "VALIDATION_SCHEMES_PATH")

        validation_shemes = GeneralsUtils.\
            read_file(validation_shemes_path)

        if schema_name not in validation_shemes:
            raise Exception("The requested validation scheme could not be found")

        return validation_shemes[schema_name]

    @staticmethod
    def translate_attribute_name(entity_name=None,
                                 entity_definitions=None,
                                 column_name=None,
                                 property_name=None):
        if entity_definitions is None:
            if entity_name is None:
                raise Exception("")

            entity_definitions = EntityUtils.get_entity_definitions(entity_name)

        if not GeneralsUtils.validate_attribute("properties", entity_definitions):
            raise Exception("")

        entity_properties = entity_definitions["properties"]

        if GeneralsUtils.validate_string(column_name):
            match_property = False

            for entity_property in entity_properties:
                if entity_properties[entity_property]["dbName"] ==\
                    column_name:
                    result = entity_property
                    match_property = True
                    break

            if not match_property:
                raise Exception("")

        elif GeneralsUtils.validate_string(property_name):
            if GeneralsUtils.validate_attribute(property_name, entity_properties):
                result = entity_properties[property_name]["dbName"]

            else:
                raise Exception("")

        else:
            raise Exception("")

        return result

    @staticmethod
    def translate_dictionary(entity_name=None,
                             entity_definitions=None,
                             table=None,
                             entity_properties=None):
        result = {}
        error_detected = None
        fail = True

        if entity_definitions is None:
            if entity_name is None:
                raise Exception("")

            entity_definitions = EntityUtils.get_entity_definitions(entity_name)

        if isinstance(table, dict):
            for column_name in table:
                try:
                    property_name = EntityUtils.translate_attribute_name(
                        entity_definitions=entity_definitions,
                        column_name=column_name)
                    result[property_name] = table[column_name]

                except Exception as error:
                    raise Exception("", error)

            fail = False

        elif isinstance(entity_properties, dict):
            for property_name in entity_properties:
                try:
                    column_name = EntityUtils.translate_attribute_name(
                        entity_definitions=entity_definitions,
                        property_name=property_name)
                    result[column_name] = entity_properties[property_name]

                except Exception as error:
                    error_detected = error

                fail = False

        if fail:
            raise Exception("", error_detected)

        return result

    @staticmethod
    def get_entity_definition(entity_name):
        # T > prefijo "entity_definition_"

        entity_definition = GeneralsUtils.\
            get_global_data("entity_definition_" + entity_name)

        if entity_definition is not None:
            return entity_definition

        entities_definitions = GeneralsUtils.\
            get_global_data("entities_definitions")

        if entities_definitions is None:
            entities_definitions_path = ConfigurationManger.get_config(
                "ENTITIES_DEFINITIONS_PATH")

            entities_definitions = GeneralsUtils.\
                read_file(entities_definitions_path)

            GeneralsUtils.set_global_data("entities_definitions",
                                          entities_definitions)

        if entity_name not in entities_definitions:
            raise Exception("Entity name not found in entities definitions")

        return entities_definitions[entity_name]    
