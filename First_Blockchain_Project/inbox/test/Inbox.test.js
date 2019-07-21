const assert = require('assert');
const ganache = require('ganache-cli');
const Web3 = require('web3');
// web3 is a instance
// ganache.provier() is provider to connect with local blockchain network which is ganache


const OPTIONS = {
    defaultBlock: "latest",
    transactionConfirmationBlocks: 1,
    transactionBlockTimeout: 5
};

const web3 = new Web3(ganache.provider(), null, OPTIONS);
const { interface, bytecode } = require('../compile');

let accounts;
let inbox;

beforeEach(async () => {
    // Get a list of all accounts
    accounts = await web3.eth.getAccounts();

    // Use one of those accounts to deploy the contract
    inbox = await new web3.eth.Contract(JSON.parse(interface)).deploy({ data: bytecode, arguments: ['Murat']}).send({ from: accounts[0], gas: '1000000'});
});

describe('Inbox', () => {
    it('deploys a contract', () => {
        assert.ok(inbox.options.address);
    });

    it('has a default message', async() => {
        const message = await inbox.methods.message().call();
        assert.equal(message, 'Murat');
    })

    it('can change the message', async () => {
        await inbox.methods.setMessage('ChangedMessage').send({ from: accounts[1]});
        const message = await inbox.methods.message().call();
        assert.equal(message, 'ChangedMessage');
    })
})



















// rinkeby.infura.io/v3/d8fa408283cb4ea9a89f4f8ca9550ce6

// Example
/* class Car{
    park() {
    return 'stopped';
    }

    drive() {
    return 'vroom';
    }
}

let car;

beforeEach(() => {
    car = new Car();
});

describe('Car', () => {
    it('Can park', () => {
        assert.equal(car.park(), 'stopped');
    });

    it('Can drive', () => {
        assert.equal(car.drive(), 'vroom');
    });
}) */