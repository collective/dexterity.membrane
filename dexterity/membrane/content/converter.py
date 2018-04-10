from dexterity.membrane.content.member import IEmail
from z3c.form.converter import BaseDataConverter
from z3c.form.interfaces import ITextWidget
import zope.component
import zope.interface
import zope.schema.interfaces


@zope.component.adapter(
    IEmail,
    ITextWidget,
)
class EmailConverter(BaseDataConverter):
    """Data converter for ITextLinesWidget operating on a frozenset."""

    def toFieldValue(self, value):
        """Convert from text lines to HTML representation."""
        # if the value is the missing value, then an empty list is produced.
        import pdb; pdb.set_trace()
        if value is self.field.missing_value:
            return u''
