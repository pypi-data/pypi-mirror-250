https://learn.microsoft.com/en-us/azure/ai-services/speech-service/quickstarts/setup-platform?tabs=linux%2Cubuntu%2Cdotnetcli%2Cdotnet%2Cjre%2Cmaven%2Cnodejs%2Cmac%2Cpypi&pivots=programming-language-python


To install OpenSSL 1.x from sources on Debian/Ubuntu based systems that don't have it, do:

	wget -O - https://www.openssl.org/source/openssl-1.1.1u.tar.gz | tar zxf -
	cd openssl-1.1.1u
	./config --prefix=/usr/local
	make -j $(nproc)
	sudo make install_sw install_ssldirs
	sudo ldconfig -v
	export SSL_CERT_DIR=/etc/ssl/certs

