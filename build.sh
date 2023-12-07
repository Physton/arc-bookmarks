#!/bin/bash

set -e

echo_success() {
    echo -e "\033[32m$1\033[0m"
}

echo_error() {
    echo -e "\033[31m$1\033[0m"
}

build() {
    platform=$1
    echo_success "========= Building for $platform ========="

    if [ "$platform" = "x86_64" ]; then
        arch_prefix="arch -x86_64"
        brew_prefix="/usr/local"
    elif [ "$platform" = "arm64" ]; then
        arch_prefix="arch -arm64"
        brew_prefix="/opt/homebrew"
    else
        echo_error "Invalid platform"
        exit 1
    fi

    eval "$($arch_prefix $brew_prefix/bin/brew shellenv)"

    if [ ! -d ./venv.$platform ]; then
        echo_success "Creating venv.$platform"
        ${brew_prefix}/bin/python3 -m venv ./venv.$platform
    fi

    # echo "Activating venv.$platform"
    # source ./venv.$platform/bin/activate

    echo_success "Installing requirements"
    $arch_prefix ./venv.$platform/bin/pip3 install -r requirements.txt

    echo_success "Building arc-bookmarks"
    build_name="arc-bookmarks.macos.$platform"
    $arch_prefix ./venv.$platform/bin/cxfreeze -c main.py --target-name=arc-bookmarks --target-dir=build/$build_name
    chmod +x build/$build_name/arc-bookmarks
    cd build
    zip -r $build_name.zip $build_name -9
    rm -rf $build_name
    cd ..

    echo_success "Build successful"
}

rm -rf build

build x86_64
build arm64