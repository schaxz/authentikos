import json, time
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

def connect_db():
    bdb_root_url = 'http://localhost:9984'
    bdb = BigchainDB(bdb_root_url)
    return bdb

def generate_key():
    alice = generate_keypair()
    return alice

def write_json(filename, bdb, alice):
    with open(filename) as json_file:
        data = json.load(json_file)
        txids = []
        for key, value in data.items():
            news_asset = {'data': {'news_agency_asset': {key: value}}}
            print(news_asset)
            metadata_checksum = {'checksum': key}
            prepared_creation_tx = bdb.transactions.prepare(operation = 'CREATE', signers = alice.public_key, asset = news_asset, metadata = metadata_checksum)
            fulfilled_creation_tx = bdb.transactions.fulfill(prepared_creation_tx, private_keys = alice.private_key)
            sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)
            time.sleep(1)
            txid = sent_creation_tx['id']
            txids.append(txid)
        return txids

def find_asset(search_term):
    retrieved_object = bdb.assets.get(search = search_term)
    return retrieved_object

if __name__ == '__main__':
    connection_choice = input("\nWelcome to Authentikos! \nWhat would you like to connect BigChainDB? [yes (y) | no (n)] \n")
    if (connection_choice == "yes" or connection_choice == "y"):
        print("\nconnecting to bigchaindb...")
        bdb = connect_db()
        print(f"\nConnection Successful! \n {bdb}")
        keypair_choice = input("\nWuld you like to gemerate a BigChainDB keypair? [yes (y) | no (n)]\n")
        # enumerate path from no -> load your own key
        if (keypair_choice == "yes" or keypair_choice == "y"):
            print("\ngenerating keys...")
            alice = generate_key()
            print(f"\nYour public key is: {alice.public_key}")
            print(f"\nYour private key is: {alice.private_key}")
            import_choice = input("\nWuld you like to write data to BigChainDB from a json file? [yes (y) | no (n)]\n")
            if (import_choice == "yes" or import_choice == "y"):
                same_dir_choice = input("\nIs your .json file in the same directory as this script?[yes (y) | no (n)]\n")
                if (same_dir_choice == "yes" or same_dir_choice == "y"):
                    filename = input("\nName of file?\n")
                    txids = write_json(filename, bdb, alice)
                    print(f"\n Transaction Succesful!\n Transaction IDs: {txids}\n Thanks for using Authentikos...bye now!") 
                elif (same_dir_choice == "no" or same_dir_choice == "n"):    
                    full_path = input("\nEnter full path to file ending in / (e.g /home/eos/hyperpartisan_news_index/ \n")
                    filename = input("\nName of file?\n")
                    full_filename = full_path + filename
                    txids = write_json(full_filename, bdb, alice)
                    print(f"\n Transaction Succesful!\n Transaction IDs: {txids}\n Thanks for using Authentikos...bye now!") 
            activity_decision = input("\nWuld you like to search for something in BigChainDB? [yes (y) | no (n)]\n")
            # enumerate while loop to keep searching if needed
            if (activity_decision == "yes" or activity_decision == "y"):
                keyword = input("\nEnter keyword to search by: \n")
                retrieved_obj_list = find_asset(keyword)
                if (len(retrieved_obj_list) == 0):
                    print("\n Your search did not return any results!")
                elif (len(retrieved_obj_list) > 0):
                    print(f"\n Your search was successful: \n {retrieved_obj_list}")         
            elif (activity_decision == "no" or activity_decision == "n"):
                print("\nThanks for using Authentikos...bye now!") 
        elif (keypair_choice == "no" or keypair_choice == "n"):
            print("\nThanks for using Authentikos...bye now!") 
    elif (connection_choice == "no" or connection_choice == "n"):
        print("\nThanks for using Authentikos...bye now!") 

