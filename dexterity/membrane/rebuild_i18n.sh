#!/bin/bash
# Run this script to update the translations.

i18ndude rebuild-pot --pot locales/dexterity.membrane.pot --create dexterity.membrane .
i18ndude sync --pot locales/dexterity.membrane.pot $(find . -name 'dexterity.membrane.po')
