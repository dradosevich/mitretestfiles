# Danny Radosevich
## users
1. Entries in the user-secrets should be encrypted in createUsers.py. Need to store the keys in user-secrets.
* username:pin combos are hashed using sha256 before being passed to write. written in the same **usr:pin** format
* written correctly to the json file

2. These secrets are used in protectSong.py. Need to look at create_metadata() and update it to include the encrypted values in the metadata instead of the un-hashed user values. This will likely include re-structuring the meta-data to accommodate larger ids.
* protect song updated to hash supplied user before using it as a key to map in the json user_secrets

3. user-secrets is used in createDevice.py to create device-secrets. We will need to update this to copy over the encrypted user entries instead of the decrypted entries.
* create device passes the plain text regions and users in, will need to hash to match the read in from user_secrets
* write out the the hashed username/passwords to the .h file for verification for the c program
* does write out the correct hashes
4. Need to decrypt these values in mb/drm_audio_fw/src/main.c in either the main function or in login - I'd do it in login.
* Values will not be decrypted. login will now need to hash the values to check the hashes against what is stored.s

##regions
1. Entries in the region-secrets should be encrypted in createRegions.py. Need to store the keys in region-secrets.
* regions are now hashed with sha256 and stored in the json regions.secrets hashed with its id

2. These secrets are used in protectSong.py. Need to look at create_metadata() and update it to include the encrypted values in the metadata instead of the decrypted region values. This will likely include re-structuring the meta-data to accommodate larger ids.

3. region-secrets is used in createDevice.py to create device-secrets. We will need to update this to copy over the encrypted region entries instead of the decrypted entries.
* create device passes the plain text regions and users in, will need to hash to match the read in from region_secrets
* write out the the hashed username/passwords to the .h file for verification for the c program
* does write out the correct hashes
4. Need to decrypt these values in mb/drm_audio_fw/src/main.c in either the main function or in login - I'd do it in login.
* Values will not be decrypted. login will now need to hash the values to check the hashes against what is stored.
