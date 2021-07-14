setup() {
    load '../bats/test_helper/bats-support/load'
    load '../bats/test_helper/bats-assert/load'
    touch ./file1
    touch ./file2
    rm ./file2
}

@test "run create_file test when file exists" {
    run exercices/verif_create_file.sh "./file1"
    assert_output 'Success'
    rm ./file1
}

@test "run create_file test when file does not exist" {
    run exercices/verif_create_file.sh "./file2"
    assert_output 'Failed'
}
