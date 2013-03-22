#!/bin/bash
# Run this script to update the translations.

../../../../bin/i18ndude rebuild-pot --pot locales/dexterity.membrane.pot --create dexterity.membrane .
../../../../bin/i18ndude sync --pot locales/dexterity.membrane.pot $(find . -name 'dexterity.membrane.po')
