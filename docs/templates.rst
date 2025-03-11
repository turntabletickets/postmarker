.. _templates:

Templates
=========

The Templates API is available via the ``templates`` manager:

.. code-block:: python

    >>> template = postmark.templates.get(983381)
    >>> template
    <Template: Test (983381)>
    >>> template.edit(Name='New name')
    >>> postmark.templates.all()
    [<Template: Test1 (983381)>, <Template: TestX (1003801)>]

Creating Templates
-----------------

Standard Templates:

.. code-block:: python

    >>> template = postmark.templates.create(
    ...     Name="Welcome Email",
    ...     Subject="Welcome to Our Service", 
    ...     HtmlBody="<html><body>Welcome, {{name}}!</body></html>",
    ...     TextBody="Welcome, {{name}}!",
    ...     Alias="welcome-email"
    ... )

Layout Templates:

.. code-block:: python

    >>> layout = postmark.templates.create(
    ...     Name="Main Layout",
    ...     Subject="{{subject}}",
    ...     HtmlBody="<html><body><header>Company Header</header>{{{content}}}<footer>Footer</footer></body></html>",
    ...     TextBody="HEADER\\n{{{content}}}\\nFOOTER",
    ...     Alias="main-layout",
    ...     TemplateType="Layout"
    ... )

Creating a Standard Template with Layout:

.. code-block:: python

    >>> template = postmark.templates.create(
    ...     Name="Welcome With Layout",
    ...     Subject="Welcome to Our Service", 
    ...     HtmlBody="<div>Welcome, {{name}}!</div>",
    ...     TextBody="Welcome, {{name}}!",
    ...     Alias="welcome-with-layout",
    ...     LayoutTemplate="main-layout"
    ... )

Filtering Templates by Type:

.. code-block:: python

    >>> standard_templates = postmark.templates.all(TemplateType="Standard")
    >>> layout_templates = postmark.templates.all(TemplateType="Layout")

Template Validation
------------------

Validating a Standard Template:

.. code-block:: python

    >>> postmark.templates.validate(Subject='Test', TextBody='Test')
    {
        'AllContentIsValid': True,
        'HtmlBody': None,
        'Subject': {
            'ContentIsValid': True,
            'RenderedContent': 'Test',
            'ValidationErrors': []
        },
        'SuggestedTemplateModel': {},
        'TextBody': {
            'ContentIsValid': True,
            'RenderedContent': 'Test',
            'ValidationErrors': []
        }
    }

Validating a Layout Template:

.. code-block:: python

    >>> postmark.templates.validate(
    ...     HtmlBody="<html><body>{{{content}}}</body></html>",
    ...     TextBody="Text: {{{content}}}",
    ...     TemplateType="Layout"
    ... )

Pushing Templates to Another Server
----------------------------------

.. note::
    Template pushing requires account-level privileges. Make sure to initialize your
    PostmarkClient with both a server token and an account token to use this feature:
    ``PostmarkClient(server_token='SERVER_TOKEN', account_token='ACCOUNT_TOKEN')``

The push_templates method allows you to push all templates from one server to another:

.. code-block:: python

    >>> source_server_id = 123456
    >>> destination_server_id = 789012
    
    # Do a dry run first to see what changes would be made without actually doing them
    >>> postmark.templates.push_templates(
    ...     SourceServerID=source_server_id, 
    ...     DestinationServerID=destination_server_id,
    ...     PerformChanges=False
    ... )
    
    # Then do the actual push
    >>> postmark.templates.push_templates(
    ...     SourceServerID=source_server_id, 
    ...     DestinationServerID=destination_server_id,
    ...     PerformChanges=True
    ... )
