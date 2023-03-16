// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Users {
    struct User {
        string id;
        string data;
    }

    mapping(string => User) private users;

    function createUser(string memory passportHash, string memory data) public {
        require(bytes(users[passportHash].id).length == 0, "User with this passport hash already exists");
        users[passportHash] = User(passportHash, data);
    }

    function getUser(string memory passportHash) public view returns (User memory) {
        require(bytes(users[passportHash].id).length > 0, "User with this passport hash does not exist");
        return users[passportHash];
    }
}
