from flask import Flask, request, jsonify
from model.LinkedList import LinkedList
from model.Node import Node
from model.Transaction import Transaction

app = Flask(__name__)
myLL = LinkedList()


@app.route('/transaction', methods=['POST'])
def add_transaction():
    """
    A method to add transactions for a specific payer and date in a sequence of calls.

    Call format example:
        { "payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z" }
        { "payer": "UNILEVER", "points": 200, "timestamp": "2022-10-31T11:00:00Z" }
        { "payer": "DANNON", "points": -200, "timestamp": "2022-10-31T15:00:00Z" }
        { "payer": "MILLER COORS", "points": 10000, "timestamp": "2022-11-01T14:00:00Z" }
        { "payer": "DANNON", "points": 1000, "timestamp": "2022-11-02T14:00:00Z" }
    """
    try:
        body = request.get_json()
        transaction = Transaction(body['payer'], body['points'], body['timestamp'])
        assert type(transaction.points) is int
    except AssertionError:
        return jsonify({'error': 'Points must be an int'}), 400
    except KeyError:
        return jsonify({'error': 'Invalid key in request body'}), 400
    except Exception:
        return jsonify({'error': 'Invalid request'}), 400

    return add_transaction_helper(transaction)


@app.route('/points', methods=['POST'])
def spend_points():
    """
    A method to spend points and return
    a list of { "payer": <string>, "points": <integer> } for each call.

    To send request format example:
        { "points": 5000 }

    Response format example:
        [
        { "payer": "DANNON", "points": -100 },
        { "payer": "UNILEVER", "points": -200 },
        { "payer": "MILLER COORS", "points": -4,700 }
        ]
    """
    spend_dict = {}  # make a dict of key payer and value points
    return_list = []
    try:
        body = request.get_json()
        points = body['points']
        head = myLL.head
        assert 0 <= points <= head.value and type(points) is int, \
            'points must be positive and less than total payer points'
    except ValueError:
        return jsonify({'error': 'Please send in a correctly formatted input'}), 400
    except AssertionError:
        return jsonify({'error': 'Please enter a positive int for points that is less than total payer points'}), 400
    except Exception:
        return jsonify({'error': 'Invalid request. Please put in the following format: { "points": <int> }'}), 400

    return spend_points_helper(head, points, return_list, spend_dict)


@app.route('/balances', methods=['GET'])
def balances():
    """
    A method to return all payer point balance after the spend call.

    Response format example:
        {
        "DANNON": 1000,
        ”UNILEVER”: 0,
        "MILLER COORS": 5300
        }
    """
    return get_balances_helper()


def add_transaction_helper(transaction):
    head = myLL.head
    curr_node = head.next
    if curr_node is None:  # first Node
        head.next = Node(transaction)
    elif transaction.timestamp < curr_node.value.timestamp:  # if current node is earlier than current head
        head.next = Node(transaction, curr_node)
    else:
        while transaction.timestamp >= curr_node.value.timestamp:
            if curr_node.next is None:  # add at end of LL
                curr_node.next = Node(transaction)
                break
            elif transaction.timestamp <= curr_node.next.value.timestamp:  # add somewhere between head and tail
                t_node = Node(transaction, curr_node.next)
                curr_node.next = t_node
                break
            else:
                curr_node = curr_node.next
    head.value += transaction.points  # add to total points count at head
    print(str(myLL))
    return jsonify({'success': 'Successfully added transaction'}), 200


def spend_points_helper(head, points, return_list, spend_dict):
    curr_node = head.next  # start after head count
    # iterate LL starting from head.next (oldest date)
    while curr_node is not None and points > 0:
        curr_payer = curr_node.value.payer
        curr_points = curr_node.value.points
        if curr_node is None:
            print('No transactions to remove points from')
            break
        # add payer to dict and subtract/add points
        if curr_points > 0:  # payer points is positive

            if curr_points <= points:  # payer points less than or equal to call points
                points -= curr_points  # subtract payer points from call points
                target_points = (curr_points * -1)
            else:  # payer points more than call points
                curr_points -= points  # subtract call points from payer points
                target_points = (points * -1)
                points = 0
        else:  # payer points is negative
            difference = abs(curr_points)
            points += difference  # add points back to call points since we need payer points positive or 0
            target_points = difference

        curr_node.value.points += target_points
        head.value += target_points

        if curr_payer not in spend_dict:
            spend_dict[curr_payer] = target_points
        else:
            spend_dict[curr_payer] += target_points

        if curr_node.next is not None:
            curr_node = curr_node.next
        else:
            break
    for key in spend_dict:
        return_list.append({"payer": key, "points": spend_dict[key]})
    return jsonify(return_list), 200


def get_balances_helper():
    payer_dict = {}
    curr_node = myLL.head.next  # start at LL head.next
    while curr_node is not None:
        curr_payer = curr_node.value.payer
        curr_points = curr_node.value.points
        if curr_node.value.payer not in payer_dict:
            payer_dict[curr_payer] = curr_points
        else:
            payer_dict[curr_payer] += curr_points
        curr_node = curr_node.next
    return jsonify(payer_dict), 200


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
