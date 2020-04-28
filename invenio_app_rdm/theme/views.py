# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020 CERN.
# Copyright (C) 2019-2020 Northwestern University.
#
# Invenio App RDM is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Blueprint used for loading templates.

The sole purpose of this blueprint is to ensure that Invenio can find the
templates and static files located in the folders of the same names next to
this file.
"""

from __future__ import absolute_import, print_function

from flask import Blueprint, current_app, render_template

from invenio_rdm_records.marshmallow.json import MetadataSchemaV1, dump_empty
from invenio_rdm_records.vocabularies import Vocabulary, dump_vocabularies

blueprint = Blueprint(
    'invenio_app_rdm',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@blueprint.route('/search')
def search():
    """Search page."""
    return render_template(current_app.config['SEARCH_BASE_TEMPLATE'])


@blueprint.route('/deposit/new')
def deposits_create():
    """Record creation page."""
    config = dict(
        apiUrl='/api/records/',
        vocabularies=dump_vocabularies(Vocabulary)
    )
    empty_record = dump_empty(MetadataSchemaV1)
    return render_template(
        current_app.config['DEPOSITS_FORMS_BASE_TEMPLATE'],
        ui_config=config,
        record=empty_record
    )


@blueprint.route('/deposit/<string:id>/edit')
def deposits_edit(id):
    """Fake deposits edit page."""
    config = dict(
        apiUrl='/api/records/',
        vocabularies=dump_vocabularies(Vocabulary))
    # minimal record
    record = {
        "_access": {
            "metadata_restricted": False,
            "files_restricted": False
        },
        "_owners": [1],
        "_created_by": 1,
        "access_right": "open",
        "id": "{}".format(id),
        "resource_type": {
            "type": "image",
            "subtype": "image-photo"
        },
        # Technically not required
        "creators": [],
        "titles": [{
            "title": "A Romans story",
            "type": "Other",
            "lang": "eng"
        }],
        "links": {
            "edit": "/deposit/{}/edit".format(id)
        }
    }
    initial_record = dump_empty(MetadataSchemaV1)
    initial_record.update(record)
    return render_template(
        current_app.config['DEPOSITS_FORMS_BASE_TEMPLATE'],
        ui_config=config,
        record=initial_record)


@blueprint.route('/deposits')
def deposits_user():
    """List of user deposits page."""
    return render_template(current_app.config['DEPOSITS_UPLOADS_TEMPLATE'])
