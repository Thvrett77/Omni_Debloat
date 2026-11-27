Name:           Omni-Debloat
Version:        1.8.0
Release:        1%{?dist}
Summary:        Omni Debloat is an application designed to debloat your android phone
License:        MIT
BuildArch:      noarch
Requires: python3
Requires: python3-qt6
Requires: android-tools
%description
Omni Debloat is an app that is designed to debloat your android smartphone using a simple ui thats going to guide you to it

%install
mkdir -p %{buildroot}/usr/bin
install -m 755 (insert dir here)Omni-Debloat-Linux.py \
    %{buildroot}/usr/bin/omni-debloat
install -m 755 (insert dir here)/adbcheck.py \
    %{buildroot}/usr/bin/adbcheck.py
%files
/usr/bin/omni-debloat
/usr/bin/adbcheck.py
