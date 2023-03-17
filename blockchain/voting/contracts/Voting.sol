// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Voting {
    struct Ballot {
        string title;
        string[] options;
        uint256 endTime;
    }

    mapping(bytes32 => Ballot) private ballots;
    mapping(bytes32 => mapping(string => bool)) private hasVoted;
    mapping(bytes32 => mapping(uint8 => uint256)) private voteCounts;

    modifier ballotExists(bytes32 _ballotAddress) {
        require(bytes(ballots[_ballotAddress].title).length > 0, "Ballot not found.");
        _;
    }

    event BallotCreated(bytes32 ballotAddress, string title, string[] options, uint256 endTime);
    event VoteCreated(bytes32 ballotAddress, string passport, uint8 option);

    function createBallot(string memory _title, string[] memory _options, uint256 _duration) external returns (bytes32) {
        bytes32 id = keccak256(abi.encodePacked(_title, block.timestamp));
        uint256 endTime = block.timestamp + _duration;
        ballots[id] = Ballot(_title, _options, endTime);
        emit BallotCreated(id, _title, _options, endTime);
        return id;
    }

    function getBallot(bytes32 _ballotAddress) ballotExists(_ballotAddress) external view returns (Ballot memory) {
        return ballots[_ballotAddress];
    }

    function hasEnded(bytes32 _ballotAddress) ballotExists(_ballotAddress) public view returns (bool) {
        return ballots[_ballotAddress].endTime < block.timestamp;
    }

    function hasVote(bytes32 _ballotAddress, string memory _passport) ballotExists(_ballotAddress) external view returns (bool) {
        return hasVoted[_ballotAddress][_passport];
    }

    function getVoteCounts(bytes32 _ballotAddress) ballotExists(_ballotAddress) external view returns (uint256[] memory) {
        uint256[] memory counts = new uint256[](ballots[_ballotAddress].options.length);
        for (uint8 i = 0; i < ballots[_ballotAddress].options.length; i++) {
            counts[i] = voteCounts[_ballotAddress][i];
        }
        return counts;
    }

    function vote(bytes32 _ballotAddress, string memory _passport, uint8 _option) ballotExists(_ballotAddress) external {
        require(!hasEnded(_ballotAddress), "Voting has ended.");
        require(_option < ballots[_ballotAddress].options.length, "Invalid option.");
        require(!hasVoted[_ballotAddress][_passport], "User has already voted.");
        hasVoted[_ballotAddress][_passport] = true;
        voteCounts[_ballotAddress][_option]++;
        emit VoteCreated(_ballotAddress, _passport, _option);
    }
}
