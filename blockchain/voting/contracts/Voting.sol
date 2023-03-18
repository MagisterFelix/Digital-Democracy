// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Voting {
    struct Ballot {
        string title;
        string[] options;
        uint256 endDate;
    }

    mapping(bytes32 => Ballot) private ballots;
    mapping(bytes32 => mapping(string => uint8)) private votes;
    mapping(bytes32 => mapping(uint8 => uint256)) private countOfVotes;

    modifier ballotExists(bytes32 _ballotId) {
        require(bytes(ballots[_ballotId].title).length > 0, "Ballot not found.");
        _;
    }

    event BallotCreated(bytes32 id, string title, string[] options, uint256 endDate);
    event VoteCreated(bytes32 ballot_id, string passport, uint8 option);

    function createBallot(string memory _title, string[] memory _options, uint256 _endDate) external {
        require(block.timestamp < _endDate, "Invalid date.");
        bytes32 id = keccak256(abi.encodePacked(_title, block.timestamp));
        ballots[id] = Ballot(_title, _options, _endDate);
        emit BallotCreated(id, _title, _options, _endDate);
    }

    function getBallot(bytes32 _ballotId) ballotExists(_ballotId) external view returns (string memory, string[] memory, uint256, uint256[] memory) {
        uint256[] memory countOfVotesByOption = new uint256[](ballots[_ballotId].options.length);
        for (uint8 i = 0; i < ballots[_ballotId].options.length; i++) {
            countOfVotesByOption[i] = countOfVotes[_ballotId][i + 1];
        }
        return (ballots[_ballotId].title, ballots[_ballotId].options, ballots[_ballotId].endDate, countOfVotesByOption);
    }

    function hasVote(bytes32 _ballotId, string memory _passport) ballotExists(_ballotId) public view returns (bool) {
        return votes[_ballotId][_passport] != 0;
    }

    function getVote(bytes32 _ballotId, string memory _passport) ballotExists(_ballotId) external view returns (uint8) {
        require(hasVote(_ballotId, _passport), "User has not voted.");
        return votes[_ballotId][_passport];
    }

    function vote(bytes32 _ballotId, string memory _passport, uint8 _option) ballotExists(_ballotId) external {
        require(block.timestamp < ballots[_ballotId].endDate, "Voting has ended.");
        require(_option != 0 && _option <= ballots[_ballotId].options.length, "Invalid option.");
        require(!hasVote(_ballotId, _passport), "User has already voted.");
        votes[_ballotId][_passport] = _option;
        countOfVotes[_ballotId][_option]++;
        emit VoteCreated(_ballotId, _passport, _option);
    }
}
