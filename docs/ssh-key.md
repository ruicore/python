# 在服务器上生成 SSH-KEY 密钥

* ssh-keygen
* 将公钥的内容放入 authorized\_keys 文件
* 将服务器的私钥匙取回本地，并放入一个文件中，文件名任意，如 test\_private
* 需要更改 test\_private 文件的权限 chmod 0600 test\_private
* 即可使用 ssh 方式登陆：ssh root@xxx.xxx.xxx.xxx  -i ~/.ssh/test\_private
* -i 表示使用指定的密钥文件
