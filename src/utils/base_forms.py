"""
=====================================================
        KEY NOTES ABOUT THE FORM FUNCTIONALITY
=====================================================
This is a forms file which basically takes
in the structure of the form for post and put
calls. It also performs basic validations necessary.

A simple immitation of rest serializers which checks
only the types and required attributes. A support for
default values and other important aspects for the
api layer can be added further in the BaseForm.

Every Form should be inherited from the BaseForm and
when called with a data object should always call is_valid
before calling the save function. If is_valid is not called
and save is called before that then the Form raises Exception

=========================================================
                        IMPORTANT
---------------------------------------------------------
Every serializer should have a 'save' method implemented.
=========================================================

If is_valid is False all the errors are stored in self._errors

Note -> Handling of is_valid() and call of save() should be
done at the views end. There is no concept of generic mixins
which performs these tasks for us (Can be implemented if needed)

I planned on using Flask-restful but since this is my own
inhouse project and I expect the values to be pretty
much precise while I am making the API calls, so I did not
need much of validations. I just implmented very core level
of required and type validations.
"""


class Field(object):
    """
    all the field based validations is performed
    here.

    This is just a basic field which doesn't even
    support validations for the emailfields. One can
    override its behaviour.
    """

    def __init__(self, options):
        self.options = options

    def is_valid(self, name, value):
        if self.options["required"] and not value:
            raise Exception("""field '{}' is a required field""".format(name))

        if not self.options["required"] and not value:
            return value

        if type(value) != self.options["type"]:
            raise Exception("""field '{}' should be of '{}' type""".format(
                name, self.options["type"].__name__))

        return self.options["type"](value)


class BaseForm(object):
    """
    Base class for all the forms declared
    it has .is_valid which returns True and False
    based on the input values and the types specified
    """

    def __init__(self, data):
        self.initial_data = data
        self._errors = []

    @classmethod
    def _get_all_fields(cls):
        fields = {}
        attributes = list(set(dir(cls)) - set(dir(object)))

        for attribute in attributes:
            if type(getattr(cls, attribute)) == Field:
                fields.update({attribute: getattr(cls, attribute)})

        return fields

    def is_valid(self, raise_exception=False):
        validated_data = {}

        fields = self.__class__._get_all_fields()

        for field_name, field_instance in fields.items():
            try:
                out = field_instance.is_valid(
                    field_name, self.initial_data.get(field_name, None))

                if not out:
                    continue

                validated_data.update({field_name: out})

            except Exception as exc:
                self._errors.append(repr(exc))

        if self._errors:
            return False

        setattr(self, 'validated_data', validated_data)

        return True

    @property
    def errors(self):
        return self._errors