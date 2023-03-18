// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Users {
    struct User {
        string fullName;
        string birthday;
    }

    mapping(string => User) private users;

    event UserCreated(string passport, string fullName, string birthday);

    function createUser(string memory _passport, string memory _fullName, string memory _birthday) external  {
        require(bytes(users[_passport].fullName).length == 0, "User already exists.");
        users[_passport] = User(_fullName, _birthday);
        emit UserCreated(_passport, _fullName, _birthday);
    }

    function getUser(string memory _passport) external view returns (User memory) {
        require(bytes(users[_passport].fullName).length > 0, "User does not exist.");
        return users[_passport];
    }
}
