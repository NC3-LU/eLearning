
var qrcode = new QRCode(document.getElementById("id-qrcode"), {
  text: window.location + "?id=ce053a70-5baf-419d-8976-757c59746081",
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
  navigator.clipboard.writeText("ce053a70-5baf-419d-8976-757c59746081");
  enableValidation();
}

function downloadTextFile() {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent("ce053a70-5baf-419d-8976-757c59746081"));
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
