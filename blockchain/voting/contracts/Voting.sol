// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Voting {
    struct Bill {
        uint256 id;
        string title;
        string[] options;
        uint256 endTime;
    }

    uint256 private nextBillId;
    mapping(uint256 => Bill) public bills;
    mapping(uint256 => mapping(string => bool)) public hasVoted;
    mapping(uint256 => mapping(uint256 => uint256)) public voteCounts;

    function createBill(string memory _title, string[] memory _options, uint256 _duration) public {
        uint256 newBillId = nextBillId++;
        uint256 endTime = block.timestamp + _duration;
        bills[newBillId] = Bill(newBillId, _title, _options, endTime);
    }

    function vote(uint256 _billId, uint256 _optionIndex, string memory _passportHash) public {
        require(bills[_billId].id != 0, "Bill not found.");
        require(block.timestamp <= bills[_billId].endTime, "Voting has ended.");
        require(_optionIndex < bills[_billId].options.length, "Invalid option index.");
        require(!hasVoted[_billId][_passportHash], "User has already voted.");

        hasVoted[_billId][_passportHash] = true;
        voteCounts[_billId][_optionIndex]++;
    }

    function getBillOptions(uint256 _billId) public view returns (string[] memory) {
        require(bills[_billId].id != 0, "Bill not found.");
        return bills[_billId].options;
    }
}

