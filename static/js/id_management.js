
var user_uuid = document.getElementById("user_uuid").textContent.trim();

var qrcode = new QRCode(document.getElementById("id-qrcode"), {
  text: window.location.origin + "?user_uuid=" + user_uuid,
  width: 128,
  height: 128,
  colorDark : "#0099ff",
  colorLight : "#ffffff",
  correctLevel : QRCode.CorrectLevel.H
});

function enableValidation() {
  var element = document.getElementById("id-management-validation");
  element.classList.remove("disabled");
}

function copyToClipboard() {
  navigator.clipboard.writeText(user_uuid);
  enableValidation();
}

function downloadTextFile() {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(user_uuid));
  element.setAttribute('download', "DAAZ - id.txt");

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);

  enableValidation();
}

function downloadQRcode() {
  var element = document.createElement('a');
  element.setAttribute('href', document.getElementById("id-qrcode").getElementsByTagName('img')[0].src);
  element.setAttribute('download', "DAAZ - QR code.png");

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);

  enableValidation();
}
