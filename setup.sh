working_dir="/home/ubuntu/bug-bounty"
mkdir -p $working_dir

if ! command -v puredns >/dev/null 2>&1; then
    echo "puredns not found, installing..."
    go install github.com/d3mondev/puredns/v2@latest
else
    echo "puredns is already installed."
fi

if ! command -v massdns >/dev/null 2>&1; then
    echo "massdns not found, installing..."
    cd /tmp &&\
    git clone https://github.com/blechschmidt/massdns.git &&\ 
    cd massdns &&\
    make &&\
    sudo make install 
else
    echo "massdns is already installed."
fi


if ! command -v dnsvalidator >/dev/null 2>&1; then
    echo "dnsvalidator not found, installing..."
    cd /tmp &&\
    git clone https://github.com/vortexau/dnsvalidator.git &&\
    cd dnsvalidator &&\
    sudo python3 setup.py install
else
    echo "puredns is already installed."
fi

cd $working_dir

# Download and filter valid resolvers, if resolvers.txt not found or older than 24hr, create new one
resolvers_filename="data/dns_bruteforce/resolvers.txt"
mkdir -p "data/dns_bruteforce"
if [ ! -f "$resolvers_filename" ] || [ $(find "$resolvers_filename" -mmin +1440) ]; then
    echo "$resolvers_filename.txt not found or older than 24 hours. Downloading..."
    dnsvalidator -tL https://raw.githubusercontent.com/trickest/resolvers/main/resolvers-community.txt -threads 100 -o $resolvers_filename
fi

# Download DNS bruteforce wordlist if not exist
wordlist_filename="data/dns_bruteforce/wordlist.txt"
if [ ! -f "$filename" ]; then
    echo "$wordlist_filename not found or older than 24 hours. Downloading..."
    wget "https://github.com/n0kovo/n0kovo_subdomains/raw/main/n0kovo_subdomains_huge.txt" -O $wordlist_filename
fi
