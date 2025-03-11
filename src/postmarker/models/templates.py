from .base import Model, ModelManager


class Template(Model):
    def __str__(self):
        return "{}: {} ({})".format(
            self.__class__.__name__,
            self._data.get("Name"),
            self._data.get("TemplateId"),
        )

    def get(self):
        new_instance = self._manager.get(self.TemplateId)
        self._data = new_instance._data
        return self

    def edit(self, **kwargs):
        response = self._manager.edit(self.TemplateId, **kwargs)
        self._update(response)
        return response

    def delete(self):
        return self._manager.delete(self.TemplateId)


class TemplateManager(ModelManager):
    name = "templates"
    model = Template
    count_key = "Count"
    offset_key = "Offset"

    def get(self, id):
        """Get a template by ID.
        
        :param id: Template ID.
        :return: :py:class:`Template`
        """
        response = self.call("GET", "/templates/%s" % id)
        return self._init_instance(response)

    def create(self, Name, Subject=None, HtmlBody=None, TextBody=None, Alias=None, TemplateType="Standard", LayoutTemplate=None):
        """Creates a template.

        :param Name: Name of template
        :param Subject: The content to use for the Subject when this template is used to send email.
        :param HtmlBody: The content to use for the HtmlBody when this template is used to send email.
        :param TextBody: The content to use for the TextBody when this template is used to send email.
        :param Alias: A custom alias to be used instead of the template ID for API calls.
        :param TemplateType: The template type. Can be either "Standard" or "Layout". Defaults to "Standard".
        :param LayoutTemplate: The layout template alias to use with this template.
        :return: :py:class:`Template`
        """
        if TemplateType == "Standard":
            assert Subject and (HtmlBody or TextBody), "Standard templates must have both Subject and either HtmlBody or TextBody"
        elif TemplateType == "Layout":
            assert not Subject, "Layout templates cannot have a Subject"
        else:
            raise ValueError("Invalid template type. Must be either 'Standard' or 'Layout'")
        data = {
            "Name": Name,
            "Subject": Subject,
            "HtmlBody": HtmlBody,
            "TextBody": TextBody,
            "Alias": Alias,
            "TemplateType": TemplateType,
            "LayoutTemplate": LayoutTemplate,
        }
        return self._init_instance(self.call("POST", "/templates", data=data))

    def edit(self, id, Name=None, Subject=None, HtmlBody=None, TextBody=None, Alias=None, TemplateType=None, LayoutTemplate=None):
        """Edit a template.
        
        :param id: Template ID.
        :param Name: Name of template
        :param Subject: The content to use for the Subject when this template is used to send email.
        :param HtmlBody: The content to use for the HtmlBody when this template is used to send email.
        :param TextBody: The content to use for the TextBody when this template is used to send email.
        :param Alias: A custom alias to be used instead of the template ID for API calls.
        :param TemplateType: The template type. Can be either "Standard" or "Layout".
        :param LayoutTemplate: The layout template alias to use with this template.
        :return: dict
        """
        data = {
            "Name": Name,
            "Subject": Subject,
            "HtmlBody": HtmlBody,
            "TextBody": TextBody,
            "Alias": Alias,
            "TemplateType": TemplateType,
            "LayoutTemplate": LayoutTemplate,
        }
        return self.call("PUT", "/templates/%s" % id, data=data)

    def all(self, Count=100, Offset=0, TemplateType=None):
        """Get all templates.
        
        :param Count: Number of templates to return per request.
        :param Offset: Number of templates to skip.
        :param TemplateType: Filter by template type. Can be either "Standard" or "Layout".
        :return: list
        """
        params = {}
        if TemplateType:
            params["TemplateType"] = TemplateType
            
        responses = self.call_many("GET", "/templates", Count=Count, Offset=Offset, **params)
        return self.expand_responses(responses, "Templates")

    def delete(self, id):
        """Delete a template.
        
        :param id: Template ID.
        :return: str
        """
        return self.call("DELETE", "/templates/%s" % id)["Message"]

    def validate(
        self,
        Subject=None,
        HtmlBody=None,
        TextBody=None,
        TestRenderModel=None,
        InlineCssForHtmlTestRender=True,
        TemplateType="Standard",
        LayoutTemplate=None,
    ):
        """Validate a template.
        
        :param Subject: The subject content to validate.
        :param HtmlBody: The HTML body content to validate.
        :param TextBody: The plain text body content to validate.
        :param TestRenderModel: The template model to be used when rendering test content.
        :param InlineCssForHtmlTestRender: Whether to inline CSS for HTML test render.
        :param TemplateType: Validates templates based on template type. Can be either "Standard" or "Layout".
        :param LayoutTemplate: An optional string to specify which layout template alias to use to validate a standard template.
        :return: dict
        """
        if TemplateType == "Standard":
            assert Subject and (HtmlBody or TextBody), "Standard templates must have both Subject and either HtmlBody or TextBody"
        elif TemplateType == "Layout":
            assert not Subject, "Layout templates cannot have a Subject"
        else:
            raise ValueError("Invalid template type. Must be either 'Standard' or 'Layout'")

        data = {
            "Subject": Subject,
            "HtmlBody": HtmlBody,
            "TextBody": TextBody,
            "TestRenderModel": TestRenderModel,
            "InlineCssForHtmlTestRender": InlineCssForHtmlTestRender,
            "TemplateType": TemplateType,
            "LayoutTemplate": LayoutTemplate,
        }
        return self.call("POST", "/templates/validate", data=data)

    def push_templates(self, SourceServerID, DestinationServerID, PerformChanges=True):
        """Push templates to another server.

        :param SourceServerID: Server ID of the source server containing the templates that will be pushed.
        :param DestinationServerID: Server ID of the destination server receiving the pushed templates.
        :param PerformChanges: Specifies whether to push templates to destination server or not. 
                        This parameter can be set to False to allow you to do a "dry-run" of the push operation.
        :return: dict
        """
        data = {
            "SourceServerID": SourceServerID,
            "DestinationServerID": DestinationServerID,
            "PerformChanges": PerformChanges
        }
        # The push templates endpoint requires account-level privileges
        return self.call("PUT", "/templates/push", data=data, token_type="account")
