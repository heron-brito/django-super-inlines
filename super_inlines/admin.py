# coding: utf-8

from __future__ import unicode_literals
from collections import defaultdict

from django.contrib.admin import helpers
from django.contrib.admin.options import InlineModelAdmin, ModelAdmin
import logging
logger = logging.getLogger(__name__)


class SuperInlineModelAdmin(InlineModelAdmin):
    inlines = ()

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        logger.warning('\n--------------  get_inline_instances  ----------------')
        logger.warning('obj')
        logger.warning(type(obj))
        logger.warning(obj)
        logger.warning('dir(obj)')
        logger.warning(dir(obj)
        logger.warning('vars(obj)')
        logger.warning(vars(obj))
        for inline_class in self.get_inlines(request, obj):
            logger.warning('inline_class')
            logger.warning(type(inline_class))
            logger.warning(inline_class)
            logger.warning('self.model')
            logger.warning(self.model)
            logger.warning('self.admin_site')
            logger.warning(self.admin_site)

            inline = inline_class(self.model, self.admin_site)
            if request:
                if not (inline.has_view_or_change_permission(request, obj) or
                        inline.has_add_permission(request, obj) or
                        inline.has_delete_permission(request, obj)):
                    continue
                if not inline.has_add_permission(request, obj):
                    inline.max_num = 0
            inline_instances.append(inline)
            #inline_instances.append(inline_class)
            

        return inline_instances
        '''    
        inline_instances = []
        for inline_class in self.inlines:
            logger.warning('inline_class')
            logger.warning(inline_class)
            logger.warning('self.model')
            logger.warning(self.model)
            logger.warning('self.admin_site')
            logger.warning(self.admin_site)
            inline = inline_class(self.model, self.admin_site)
            if request:
                if not (inline.has_add_permission(request) or
                        inline.has_change_permission(request, obj) or
                        inline.has_delete_permission(request, obj)):
                    continue
                if not inline.has_add_permission(request):
                    inline.max_num = 0
            inline_instances.append(inline)

        return inline_instances
        '''

    def get_formsets_with_inlines(self, request, obj=None):
        """
        Yields formsets and the corresponding inlines.
        """
        logger.warning('\n--------------  get_formsets_with_inlines  ----------------')        
        for inline in self.get_inline_instances(request, obj):
            yield inline.get_formset(request, obj), inline

    def _create_formsets(self, request, obj, change, index, is_template):
        "Helper function to generate formsets for add/change_view."
        logger.warning('\n--------------  _create_formsets  ----------------')          
        formsets = []
        inline_instances = []
        prefixes = defaultdict(int)
        get_formsets_args = [request]
        if change:
            get_formsets_args.append(obj)
        base_prefix = self.get_formset(request).get_default_prefix()
        for FormSet, inline in self.get_formsets_with_inlines(
                *get_formsets_args):
            prefix = base_prefix + '-' + FormSet.get_default_prefix()
            if not is_template:
                prefix += '-%s' % index
            prefixes[prefix] += 1
            if prefixes[prefix] != 1 or not prefix:
                prefix = "%s-%s" % (prefix, prefixes[prefix])
            formset_params = {
                'instance': obj,
                'prefix': prefix,
                'queryset': inline.get_queryset(request),
            }
            if request.method == 'POST':
                formset_params.update({
                    'data': request.POST,
                    'files': request.FILES,
                    'save_as_new': '_saveasnew' in request.POST
                })
            formset = FormSet(**formset_params)
            formset.has_parent = True
            formsets.append(formset)
            inline_instances.append(inline)
        return formsets, inline_instances

    def get_inline_formsets(self, request, formsets, inline_instances,
                            obj=None):
        logger.warning('\n--------------  get_inline_formsets  ----------------')          
        inline_admin_formsets = []
        for inline, formset in zip(inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            readonly = list(inline.get_readonly_fields(request, obj))
            prepopulated = dict(inline.get_prepopulated_fields(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                fieldsets, prepopulated, readonly, model_admin=self)
            inline_admin_formsets.append(inline_admin_formset)
        return inline_admin_formsets


class SuperModelAdmin(ModelAdmin):
    def _create_formsets(self, request, obj, change):
        logger.warning('\n--------------  SuperModelAdmin: _create_formsets  0.0.1 ----------------')        
        formsets, inline_instances = super(
            SuperModelAdmin, self)._create_formsets(request, obj, change)
        logger.warning(inline_instances)
        for formset, inline_instance in zip(formsets, inline_instances):
            logger.warning(inline_instances)
            if not isinstance(inline_instance, SuperInlineModelAdmin):
                continue
            for index, form in enumerate(formset.forms):
                new_formsets, new_inline_instances = \
                    inline_instance._create_formsets(request, form.instance,
                                                     change, index, False)
                # If an empty inline form has non-empty sub-inline instances,
                # we force the save of that empty inline, so that it will be
                # validated.
                if any(new_form.has_changed() for new_formset in new_formsets
                       for new_form in new_formset):
                    form.has_changed = lambda: True

                formsets.extend(new_formsets)
                inline_instances.extend(new_inline_instances)
        logger.warning('inline_instances')
        logger.warning(inline_instances)
        logger.warning('dir(inline_instances)')
        logger.warning(dir(inline_instances))
        logger.warning('vars(inline_instances)')
        logger.warning(vars(inline_instances))
        logger.warning('formset')
        logger.warning(formsets)
        return formsets, inline_instances
