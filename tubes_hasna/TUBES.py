#TUGAS BESAR JARINGAN KOMPUTER - Kelompok 8  - IF 45 01
#Ekfa Ediet Hamara (1301213360) - Hasna Rafida Alya (1301213061) - Naufal Yazid Zachary (1301213001)

import socket #mengimport soket
import os #mengimport Operating System

def handle_request(request): #menangani request yang diterima oleh server
    request_lines = request.split("\r\n") #memisahkan baris request menjadi elemen-elemen terpisah dalam bentuk daftar (list).
    method, path, _ = request_lines[0].split(" ")  #memisahkan baris pertama request menjadi daftar list dengan 3 elemen
    message_body = "<html><body><h1>Tugas Besar Jaringan Komputer</h1></body></html>"  #string untuk tampilan web

    if method == "GET": #metode HTTP yang digunakan yaitu GET untuk mengambil data dari server
        if path == "/": #memriksa path yang diterima dalam permintaan HTTP
            path = "/index.html" #file index html
        file_path = os.path.join("tubes", path[1:]) #menghasilkan path file yang tepat berdasarkan path yang diterima dalam permintaan HTTP.

        if os.path.exists(file_path): #memeriksa apakah file yang sesuai dengan file_path ada di sistem file.
            response_line = "HTTP/1.1 200 OK\r\n" #request berhasil
            content_type = "Content-Type: text/html\r\n\r\n" #dikirimkan dalam format HTML
            with open(file_path, "r") as file: #buka file
                message_body = file.read()
        else:
            response_line = "HTTP/1.1 404 Not Found\r\n" #request gagal
            content_type = "Content-Type: text/html\r\n\r\n"#dikirimkan dalam format HTML
            message_body = "<html><body><h1>404 Not Found</h1></body></html>" #HTML merespon jika file diminta tdk ditemukan (404 Not Found)
    else:
        response_line = "HTTP/1.1 400 Bad Request\r\n" #kesalahan dalam request yg diterima
        content_type = "Content-Type: text/html\r\n\r\n" #teks HTML
        message_body = "<html><body><h1>400 Bad Request</h1></body></html>" #HTML menampilkan pesan "400 Bad Request" 

    response = response_line + content_type + message_body #membentuk respons HTTP lengkap dalam variabel response
    return response

def tcp_server():
     #server address and port
    SERVER_HOST = "127.0.0.1" #alamat lokal
    SERVER_PORT = 80 #port yang digunakan

    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#membuat objek baru dimana AF_INET: alamat berbasis pada IPv4 dan SOCK_STREAM: socket TCP
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#menyetel opsi socket yaitu SOLSOCKET(menentukan level opsi socket),
    #SO_REUSEADDR(menentukan opsi socket yang akan diatur), 1(menentukan nilai untuk menyetel opsi)
    socket_server.bind((SERVER_HOST, SERVER_PORT))#mengubungkan alamat IP dengan nomor port ke socket

    socket_server.listen()#server menerima koneksi

    print("Server ready to launch")

    while True: #melakukan loop
        sock_client, client_address = socket_server.accept()#menerima koneksi yang akan masuk untuk membuat koneksi TCP baru dari klien yang akan mengembalikan 
         #sock_client(Objek baru untuk mengirim dan menerima data selama terhubung) dan client_address(alamat klien) 
        request = sock_client.recv(1024).decode()#menerima respon dari server dengan menentukan jumlah maks data yang akan diterima menggunakan 
         #.decode() maka akan menerjemahkan byte ke string

        print("Request from client:", request) #mencetak "Dari Client"

        response = handle_request(request) #memproses permintaan yang diterima dan menghasilkan respons yang sesuai
        sock_client.send(response.encode()) #mengirim respon HTTP yg telah diubah representasi  byte

        sock_client.close()#menutup socket client

    socket_server.close()

if __name__ == "__main__": #menjalankan server yang telah didefinisikan sebelumnya
    tcp_server() #implementasi untuk run server TCP

