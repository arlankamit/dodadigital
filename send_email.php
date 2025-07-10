<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = htmlspecialchars(trim($_POST['name']));
    $email = htmlspecialchars(trim($_POST['email']));
    $phone = htmlspecialchars(trim($_POST['phone']));
    $message = htmlspecialchars(trim($_POST['message']));

    $to = "office@dodadigital.kz";
    $subject = "Новая заявка с сайта DODA Digital";
    $body = "Имя: $name\nEmail: $email\nТелефон: $phone\nСообщение:\n$message";
    $headers = "From: no-reply@dodadigital.kz\r\n";
    $headers .= "Reply-To: $email\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

    if (mail($to, $subject, $body, $headers)) {
        http_response_code(200);
        echo json_encode(["message" => "Заявка успешно отправлена"]);
    } else {
        http_response_code(500);
        echo json_encode(["message" => "Ошибка при отправке заявки"]);
    }
} else {
    http_response_code(400);
    echo json_encode(["message" => "Неверный метод запроса"]);
}
?>
