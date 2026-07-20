(function () {
  var pendingForm = null;
  var confirmModal = null;
  var crudModal = null;

  function getCrudModal() {
    var modalEl = document.getElementById("crudModal");
    if (!modalEl || !window.bootstrap) {
      return null;
    }
    crudModal = crudModal || bootstrap.Modal.getOrCreateInstance(modalEl);
    return crudModal;
  }

  function getConfirmModal() {
    var modalEl = document.getElementById("crudSaveConfirmModal");
    if (!modalEl || !window.bootstrap) {
      return null;
    }
    confirmModal = confirmModal || bootstrap.Modal.getOrCreateInstance(modalEl);
    return confirmModal;
  }

  function initSelect2(scope) {
    if (!window.jQuery || !jQuery.fn.select2) {
      return;
    }

    var $scope = scope ? jQuery(scope) : jQuery(document);
    $scope.find("select.select2").each(function () {
      var $select = jQuery(this);
      if ($select.data("select2")) {
        return;
      }
      $select.select2({
        width: "100%",
        dropdownParent: jQuery("#crudModal").length ? jQuery("#crudModal") : jQuery(document.body),
        placeholder: $select.attr("placeholder") || "Pilih data",
        allowClear: !$select.prop("required")
      });
    });
  }

  document.addEventListener("show.bs.modal", function (event) {
    if (event.target.id !== "crudModal") {
      return;
    }

    var trigger = event.relatedTarget;
    var title = trigger ? trigger.getAttribute("data-crud-modal-title") : "";
    var titleEl = document.getElementById("crudModalLabel");
    var bodyEl = document.getElementById("crud-modal-body");

    if (title && titleEl) {
      titleEl.textContent = title;
    }

    if (bodyEl) {
      bodyEl.innerHTML = '<div class="crud-modal-loading"><div class="spinner-border text-primary" role="status"></div></div>';
    }
  });

  document.addEventListener("htmx:afterSwap", function (event) {
    initSelect2(event.target);
  });

  document.addEventListener("submit", function (event) {
    var form = event.target;
    if (!form.matches('form[data-confirm="save"]') || form.dataset.confirmed === "true") {
      return;
    }

    event.preventDefault();
    pendingForm = form;

    var modal = getConfirmModal();
    if (modal) {
      modal.show();
      return;
    }

    form.dataset.confirmed = "true";
    if (window.htmx && form.hasAttribute("hx-post")) {
      htmx.trigger(form, "submit");
    } else {
      form.submit();
    }
  }, true);

  document.addEventListener("click", function (event) {
    var confirmButton = event.target.closest("#crudConfirmSaveButton");
    if (!confirmButton) {
      return;
    }

    if (!pendingForm) {
      return;
    }

    pendingForm.dataset.confirmed = "true";
    var modal = getConfirmModal();
    if (modal) {
      modal.hide();
    }

    if (pendingForm.requestSubmit) {
      pendingForm.requestSubmit();
    } else {
      pendingForm.submit();
    }
  });

  document.body.addEventListener("crudSuccess", function () {
    var modal = getCrudModal();
    if (modal) {
      modal.hide();
    }
    window.setTimeout(function () {
      window.location.reload();
    }, 250);
  });

  document.body.addEventListener("crudError", function () {
    initSelect2(document.getElementById("crud-modal-body"));
  });

  document.addEventListener("DOMContentLoaded", function () {
    initSelect2(document);
  });
})();
