def process_transactions(logs):
    transaction_status = {'action': [], 'transaction': []}
    checkpoint_reached = False

    for entry in reversed(logs):
        parts = entry[1:-1].split(' ')
        
        if 'CKPT' in parts[0]:
            checkpoint_reached = True
        elif parts[0] == 'COMMIT' and checkpoint_reached:
            transaction_status['action'].append('ignore')
            transaction_status['transaction'].append(parts[1])
        elif parts[0] == 'COMMIT':
            transaction_status['action'].append('redo')
            transaction_status['transaction'].append(parts[1])
        elif parts[0] == 'START' and parts[1] not in transaction_status['transaction']:
            transaction_status['action'].append('undo')
            transaction_status['transaction'].append(parts[1])

    return transaction_status

def process_variable_values(logs, transaction_status):
    final_values = {'variable': [], 'value': []}

    for entry in logs:
        parts = entry[1:-1].split(' ')
        
        if len(parts) != 4 or parts[1] in final_values['variable']:
            continue
        
        if parts[0] in transaction_status['transaction']:
            index = transaction_status['transaction'].index(parts[0])
        else:
            continue
        
        if transaction_status['action'][index] == 'redo':
            final_values['variable'].append(parts[1])
            final_values['value'].append(parts[3])
        elif transaction_status['action'][index] == 'undo':
            final_values['variable'].append(parts[1])
            final_values['value'].append(parts[2])
        elif transaction_status['action'][index] == 'ignore':
            final_values['variable'].append(parts[1])
            final_values['value'].append(parts[3])

    return final_values

def main():
    with open("log.txt", 'r') as file:
        logs = file.read().splitlines()
    
    transaction_status = process_transactions(logs)

    for i in range(len(transaction_status['action'])):
        print(f"{transaction_status['action'][i]} - {transaction_status['transaction'][i]}")
    
    final_values = process_variable_values(logs, transaction_status)

    print("\nFinal variable values:")
    for i in range(len(final_values['variable'])):
        print(f"{final_values['variable'][i]} = {final_values['value'][i]}")

if __name__ == '__main__':
    main()