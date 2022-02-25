Recipe
======

.. py:method:: recipe.findrecipe( request: Request, length: int, keywords: Union[str, None] = None)
    :async:

    Requests user settings and search for recipe.
    
    :param request: the http request
    :type request: starlette.requests.Request

    :param length: the minimal length
    :type length: int

    :param keywords: the keywords. Defaults to None.
    :type keywords: Union[str, None], optional

    :return: the http response
    :rtype: TemplateResponse