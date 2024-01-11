# Logging
import logging

try:
    # import django_graphbox
    import graphene
    from django_graphbox.builder import SchemaBuilder
    # import auditor models
    from django_auditor_logs.models import audits_models

    class AuditorSchemaBuilder(SchemaBuilder):
        """Schema builder for Auditor"""

        def __init__(self, session_manager=None, access_group=None, pagination_length=20, pagination_style='paginated', validators_by_operation={}):
            super().__init__(session_manager)
            for model_name in audits_models.keys():
                self.add_model(
                    audits_models[model_name],
                    access_group=access_group,
                    pagination_length=pagination_length,
                    pagination_style=pagination_style,
                    ordering_field='-date',
                    operations_to_build=['list_field'],
                    external_filters=[
                        {
                            'field_name': 'id_model',
                            'param_name': 'id_model',
                            'param_type': graphene.Int()
                        },
                        {
                            'field_name': 'action',
                            'param_name': 'action',
                            'param_type': graphene.String()
                        },
                        {
                            'field_name': 'date',
                            'param_name': 'date',
                            'param_type': graphene.DateTime()
                        },
                    ],
                    validators_by_operation=validators_by_operation
                )

        def build_auditor_schema(self):
            """Builds the Auditor schema"""
            return self.build_schema_query()

except ImportError:
    logging.error("django_graphbox=>1.2.10 not installed. Please install it to use the AuditorSchemaBuilder")