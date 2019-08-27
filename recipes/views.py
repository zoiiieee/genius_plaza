from formtools.wizard.views import SessionWizardViewfrom recipes import forms as recipe_formsfrom recipes.models import RecipeModel, IngredientModel, StepModelfrom django.db import transactionfrom django.shortcuts import redirectclass CreateRecipeView(SessionWizardView):    template_name = "recipes/create_recipe.html"    success_url = '/new-recipe-success/'    form_list = [        ("recipe", recipe_forms.RecipeDetailsForm),        ("ingredients", recipe_forms.IngredientFormSet),        ("steps", recipe_forms.StepFormSet),        ("confirmation", recipe_forms.ConfirmationStep)    ]    template_dict = {        'confirmation': 'recipes/confirm_recipe.html'    }    def get_template_names(self):        return [self.template_dict.get(self.steps.current, self.template_name)]    def test_func(self):        return hasattr(self, 'user')    def get_context_data(self, form, **kwargs):        context = super().get_context_data(form, **kwargs)        if self.steps.current == 'confirmation':            recipe = self.get_all_cleaned_data()            ingredients = recipe.pop('formset-ingredients', None)            steps = recipe.pop('formset-steps', None)            context.update({                'recipe': recipe,                'ingredients': ingredients,                'steps': steps            })        return context    def done(self, form_list, **kwargs):        cleaned_data = self.get_all_cleaned_data()        ingredients = cleaned_data.pop('formset-ingredients', None)        steps = cleaned_data.pop('formset-steps', None)        with transaction.atomic():            recipe = RecipeModel(**cleaned_data)            recipe.save()            for ingredient in ingredients:                ingredient['recipe'] = recipe                IngredientModel.objects.create(**ingredient)            for step in steps:                step['recipe'] = recipe                StepModel.objects.create(**step)        return redirect(self.success_url)