"""
Generic views untuk Excel import/export
Bisa di-inherit di setiap app
"""
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from config.utils.excel_handler import ExcelExporter, ExcelImporter


class ExcelExportView(View):
    """Generic view untuk download data sebagai Excel"""
    
    model = None
    filename_pattern = "{model}_{timestamp}.xlsx"
    columns = None  # Jika None, ambil dari model fields
    
    def get_filename(self):
        """Generate nama file"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        model_name = self.model._meta.model_name
        return self.filename_pattern.format(model=model_name, timestamp=timestamp)
    
    def get_queryset(self):
        """Override untuk custom filtering"""
        return self.model.objects.all()
    
    def get(self, request, *args, **kwargs):
        """Handle GET request - langsung download Excel dengan semua kolom"""
        return self.download_view(request)
    
    def form_view(self, request):
        """Tampilkan form untuk memilih opsi export"""
        fields = []
        for field in self.model._meta.get_fields():
            if not field.is_relation and not field.many_to_many:
                fields.append({
                    'name': field.name,
                    'verbose_name': field.verbose_name,
                    'selected': True  # Default semua selected
                })
        
        return render(request, 'components/excel/export.html', {
            'model_name': self.model._meta.verbose_name_plural,
            'fields': fields,
        })
    
    def download_view(self, request):
        """Download Excel dengan opsi yang dipilih"""
        queryset = self.get_queryset()
        
        # Filter berdasarkan q
        q = request.GET.get('q')
        if q:
            # Simple search, bisa di-override
            search_fields = []
            for field in self.model._meta.get_fields():
                if not field.is_relation and not field.many_to_many and field.__class__.__name__ in ['CharField', 'TextField']:
                    search_fields.append(f"{field.name}__icontains")
            if search_fields:
                from django.db.models import Q
                query = Q()
                for field in search_fields:
                    query |= Q(**{field: q})
                queryset = queryset.filter(query)
        
        # Pilih kolom
        columns = request.GET.getlist('columns')
        if not columns:
            columns = None  # Semua kolom
        
        exporter = ExcelExporter(
            model=self.model,
            queryset=queryset,
            columns=columns,
            title=self.model._meta.verbose_name_plural
        )
        
        excel_data = exporter.export()
        
        response = HttpResponse(
            excel_data,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{self.get_filename()}"'
        
        return response


class ExcelImportView(TemplateView):
    """Generic view untuk upload & import Excel dengan preview"""
    
    model = None
    template_name = 'components/excel/import.html'
    success_url = None
    columns = None  # Jika None, ambil dari model fields
    match_fields = None
    
    def _get_default_columns(self):
        """Get default columns dari model"""
        from config.utils.excel_handler import ExcelImporter
        importer = ExcelImporter(model=self.model, file_stream=b'')
        return importer._get_default_columns()
    
    def get_success_url(self):
        """Redirect URL setelah import sukses"""
        if self.success_url:
            return self.success_url
        return self.request.GET.get('next', '/')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        context['model_name'] = self.model._meta.verbose_name_plural
        context['columns'] = self.columns or self._get_default_columns()
        context['import_url'] = self.request.get_full_path()
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle POST - process uploaded file"""
        action = request.POST.get('action')
        
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'File tidak ditemukan'}, status=400)
        
        file = request.FILES['file']
        
        try:
            importer = ExcelImporter(
                model=self.model,
                file_stream=file.read(),
                columns=self.columns,
                match_fields=self.match_fields,
                filename=file.name,
            )
            
            # Step 1: Preview
            if action == 'preview':
                data = importer.read_excel()
                importer.validate(data)

                if importer.read_errors or importer.empty_file_error:
                    return JsonResponse({
                        'status': 'error',
                        'errors': importer.errors,
                    }, status=400)
                
                return JsonResponse({
                    'status': 'preview',
                    'preview': importer.preview_data,
                    'has_errors': len(importer.errors) > 0,
                    'errors': importer.errors
                })
            
            # Step 2: Import
            elif action == 'import':
                result = importer.import_data()
                
                if result['success']:
                    message_parts = [f"{result['imported']} data ditambahkan"]
                    if result.get('updated'):
                        message_parts.append(f"{result['updated']} data diperbarui")
                    if result.get('skipped'):
                        message_parts.append(f"{result['skipped']} data dilewati")

                    success_message = "✅ Proses import selesai: " + ', '.join(message_parts)

                    messages.success(
                        request,
                        success_message
                    )
                    return JsonResponse({
                        'status': 'success',
                        'imported': result['imported'],
                        'updated': result['updated'],
                        'skipped': result.get('skipped', 0),
                        'redirect': self.get_success_url()
                    })
                else:
                    return JsonResponse({
                        'status': 'error',
                        'errors': result['errors'],
                        'preview': result['preview'],
                        'imported': result['imported'],
                        'updated': result.get('updated', 0),
                        'skipped': result.get('skipped', 0),
                    })
        
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'errors': [str(e)]
            })


class GenericExcelExportView(ExcelExportView):
    """Generic view untuk export berdasarkan app.model"""
    
    def dispatch(self, request, app_label, model_name, *args, **kwargs):
        # Set model dynamically
        from django.apps import apps
        self.model = apps.get_model(app_label, model_name)
        return super().dispatch(request, *args, **kwargs)


class GenericExcelImportView(ExcelImportView):
    """Generic view untuk import berdasarkan app.model"""
    
    def dispatch(self, request, app_label, model_name, *args, **kwargs):
        # Set model dynamically
        from django.apps import apps
        self.model = apps.get_model(app_label, model_name)
        return super().dispatch(request, *args, **kwargs)


class ExcelMixin:
    """Mixin untuk menambah export/import ke CRUD view"""
    
    enable_excel = True
    excel_columns = None  # Custom columns untuk Excel
    
    def get_excel_columns(self):
        """Override untuk custom columns"""
        return self.excel_columns
    
    def get_export_queryset(self):
        """Override untuk custom filtering saat export"""
        return self.get_queryset()
    
    def get_context_data(self, **kwargs):
        """Add excel URLs ke context"""
        context = super().get_context_data(**kwargs)

        if not self.enable_excel:
            context['export_url'] = None
            context['import_url'] = None
            return context

        context['export_url'] = self.get_export_url()
        context['import_url'] = self.get_import_url()
        return context
    
    def get_export_url(self):
        """Override untuk set custom export URL"""
        if hasattr(self, 'url_export') and self.url_export:
            from django.urls import reverse
            return reverse(self.url_export)
        # Fallback to generic URL
        from django.urls import reverse
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return reverse('config:generic_excel_export', kwargs={'app_label': app_label, 'model_name': model_name})
    
    def get_import_url(self):
        """Override untuk set custom import URL"""
        if hasattr(self, 'url_import') and self.url_import:
            from django.urls import reverse
            return reverse(self.url_import)
        # Fallback to generic URL
        from django.urls import reverse
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return reverse('config:generic_excel_import', kwargs={'app_label': app_label, 'model_name': model_name})
