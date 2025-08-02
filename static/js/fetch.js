document.addEventListener('DOMContentLoaded', function() {
  const btn = document.getElementById('openNotification');
  const btn2 = document.getElementById('openNotification2');
  const notify = document.getElementById('notifyOn');
  const notify2 = document.getElementById('notifyOn2');
  if (btn) {
    btn.addEventListener('click', function() {
        notify.style.display = 'none';
        fetch('/logs/viewed/', {
            method: 'GET',
            credentials: 'include',
            headers: {
            'Accept': 'application/json'
            }
        });
    });
  }

  if (btn2) {
    btn2.addEventListener('click', function() {
        notify2.style.display = 'none';
        fetch('/logs/viewed/', {
            method: 'GET',
            credentials: 'include',
            headers: {
            'Accept': 'application/json'
            }
        });
    });
  }

});
