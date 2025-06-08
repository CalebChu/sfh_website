document.addEventListener("DOMContentLoaded", () => {
    const qrcode = document.getElementById("qr-code");
    const url = window.location.origin+"/p/event_attendance_confirmation/";
    new QRCode(qrcode, {
        "text": url+qrcode.getAttribute("value"),
        "colorDark" : "#18191b",
        "colorLight" : "#f5f4f2", 
    });
    qrcode.setAttribute("href", url+qrcode.getAttribute("value"));
});