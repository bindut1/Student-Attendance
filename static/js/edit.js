(function() {
  function setupImagePreview() {
    var input = document.getElementById('id_avatar');
    var img = document.querySelector('.avatar-img');

    if (input && img) {
      input.onchange = function() {
        if (this.files && this.files[0]) {
          var reader = new FileReader();
          reader.onload = function(e) {
            img.src = e.target.result;
          };
          reader.readAsDataURL(this.files[0]);
        }
      };
    }
  }

  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(setupImagePreview, 1);
  } else {
    document.addEventListener('DOMContentLoaded', setupImagePreview);
  }
})();