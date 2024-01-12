"""
Validate the submission.
"""

import os
import sys

from ciocore.validator import Validator
from cionuke import const as k
from cionuke.components import frames
from cionuke import submit


import json

class ValidateTaskCount(Validator):
    def run(self, _):
        main_seq, scout_seq = frames.get_sequences(self._submitter)

        count = len(main_seq.chunks())
        if count > 1000:
            self.add_warning(
                "This submission contains over 1000 tasks ({}). Are you sure this is correct?".format(
                    count
                )
            )

class ValidateOutputPath(Validator):
    def run(self, _):

        submission = submit.resolve_submission(submitter=self._submitter, should_scrape_assets=True)
        output_path = submission['output_path']

        if not output_path:
            self.add_error("The Conductor output path has not been set. Please ensure the the file knob on your Write nodes is properly set.")
            return

        invalid_asset_paths = []

        
        for p in submission['upload_paths']:

            if os.path.abspath(p).startswith(os.path.abspath(output_path)):
                invalid_asset_paths.append(p)

        if invalid_asset_paths:
            self.add_error(
                "This submission contains dependencies that are located within the output path ({}). The output path can not be the root of any files being uploaded as part of this job.\n\nPlease change the output path to a more specific folder.\n\n\t{}".format(
                    output_path, "\n\t".join(invalid_asset_paths)
                )
            )

def run(submitter):

    meta_warnings = set()

    validators = [plugin(submitter) for plugin in Validator.plugins()]

    for validator in validators:
        try:
            validator.run(None)
        except BaseException as ex:
            meta_warnings.add(
                "[{}]:\nValidator failed to run. Don't panic, it's probably due to an unsupported feature and can be ignored.\n{}".format(
                    validator.title(), str(ex)
                )
            )

    return {
        "error": list(set.union(*[validator.errors for validator in validators])),
        "warning": list(set.union(*[validator.warnings for validator in validators]))
        + list(meta_warnings),
        "info": list(set.union(*[validator.notices for validator in validators])),
    }

