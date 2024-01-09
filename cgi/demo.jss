#!C:/nodejs/node.exe

let envs = "<ul>";
for( let key in process.env ) {
    envs += `<li>${key} = ${process.env[key]}</li>`;
}
envs += "</ul>";

process.stdout.write("Content-Type: text/html\r\n");
process.stdout.write("\r\n");
process.stdout.write(`<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CGI</title>
</head>
<body>
    <h1>CGI працює з JS</h1>
    <p>${envs}</p>
</body>
</html>`);