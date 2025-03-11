from postmarker.models.templates import Template

CASSETTE_NAME = "templates"


class TestModel:
    def test_repr(self, template):
        assert str(template) == "Template: Test (983381)"

    def test_default(self, template):
        assert isinstance(template, Template)

    def test_get(self, template):
        instance = template.get()
        assert isinstance(instance, Template)

    def test_edit(self, template):
        response = template.edit(Name="Test")
        assert response == {
            "Active": True,
            "Name": "Test",
            "TemplateId": 983381,
        }
        # Verify that the instance was updated
        assert template.Name == "Test"


class TestManager:
    def test_edit(self, postmark):
        assert postmark.templates.edit(983381, Name="Test1") == {
            "Active": True,
            "Name": "Test1",
            "TemplateId": 983381,
        }

    def test_all(self, postmark):
        response = postmark.templates.all()
        assert len(response) == 1
        assert isinstance(response[0], Template)
        
    def test_all_with_type(self, postmark):
        response = postmark.templates.all(TemplateType="Standard")
        assert len(response) >= 0
        if response:
            assert isinstance(response[0], Template)

    def test_create(self, postmark):
        template = postmark.templates.create(Name="TestX", Subject="TestSubj", TextBody="Test content")
        assert isinstance(template, Template)
        assert template.Name == "TestX"
        assert template.delete() == "Template 1003802 removed."
        
    def test_create_with_layout(self, postmark):
        # First create a layout template
        layout_template = postmark.templates.create(
            Name="Layout Test", 
            Subject="Layout Subject", 
            HtmlBody="<html><body>{{{content}}}</body></html>", 
            Alias="test-layout", 
            TemplateType="Layout"
        )
        
        # Then create a standard template using the layout
        template = postmark.templates.create(
            Name="Standard with Layout", 
            Subject="Test with Layout",
            HtmlBody="<p>Content to be inserted in layout</p>", 
            TemplateType="Standard",
            LayoutTemplate="test-layout"
        )
        
        assert isinstance(template, Template)
        assert template.TemplateType == "Standard"
        assert template.LayoutTemplate == "test-layout"
        
        # Clean up
        template.delete()
        layout_template.delete()

    def test_validate(self, postmark):
        response = postmark.templates.validate(Subject="Test", TextBody="Test")
        assert response == {
            "AllContentIsValid": True,
            "HtmlBody": None,
            "Subject": {
                "ContentIsValid": True,
                "RenderedContent": "Test",
                "ValidationErrors": [],
            },
            "SuggestedTemplateModel": {},
            "TextBody": {
                "ContentIsValid": True,
                "RenderedContent": "Test",
                "ValidationErrors": [],
            },
        }
        
    def test_validate_layout(self, postmark):
        response = postmark.templates.validate(
            HtmlBody="<html><body>{{{content}}}</body></html>",
            TextBody="Text: {{{content}}}",
            TemplateType="Layout"
        )
        assert response["AllContentIsValid"] == True
        
    def test_push_templates(self, postmark, server):
        # Note: This requires an account token to be set
        # This test assumes the existence of at least two servers
        source_server_id = server.ID
        # For testing purposes, we'll use the same server as both source and destination
        destination_server_id = server.ID
        
        # Test dry run first (PerformChanges=False)
        response = postmark.templates.push_templates(
            SourceServerID=source_server_id,
            DestinationServerID=destination_server_id,
            PerformChanges=False
        )
        assert isinstance(response, dict)
        
        # Then test actual push
        response = postmark.templates.push_templates(
            SourceServerID=source_server_id,
            DestinationServerID=destination_server_id,
            PerformChanges=True
        )
        assert isinstance(response, dict)
