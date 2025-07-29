from rest_framework.exceptions import ValidationError


class OptionsBelongToQuestionValidator:
    requires_context = True

    def __init__(self, question_field, options_field):
        self.q_field = question_field
        self.opts_field = options_field

    def __call__(self, attrs, serializer):
        question = attrs.get(self.q_field)
        opts = attrs.get(self.opts_field, [])
        bad = [o.pk for o in opts if o.question_id != question.pk]
        if bad:
            raise ValidationError({
                self.opts_field: f"Option(s) {bad} don't belong to question {question.pk}"
            })
