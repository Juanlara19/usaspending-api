from django.utils.decorators import method_decorator
from usaspending_api.common.exceptions import InvalidParameterException
from usaspending_api.awards.v2.filters.filter_helpers import transform_keyword

API_TRANSFORM_FUNCTIONS = [transform_keyword]


def api_transformations(api_version, function_list):
    """
    Decorator designed to transform request object from API call to allow for backwards
    compatibility between API versions. Functions being passed to this decorator should
    accept a request object, and return it after modifications.
    """

    def class_based_decorator(ClassBasedView):
        def view_func(function):
            def wrap(request, *args, **kwargs):
                for func in function_list:
                    try:
                        request = func(request, api_version)
                    except InvalidParameterException:
                        raise
                return function(request, *args, **kwargs)

            return wrap

        ClassBasedView.post = method_decorator(view_func)(ClassBasedView.post)
        return ClassBasedView

    return class_based_decorator
