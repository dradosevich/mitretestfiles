#!/usr/bin/env python3
"""
Description: Protects song by adding metadata or any other security measures
Use: Once per song
"""
import json
import struct
import os
import wave
import hashlib
from argparse import ArgumentParser
import numpy as np


class ProtectedSong(object):
    """Example song object for protected song"""

    def __init__(self, path_to_song, metadata):
        """initialize values
        Args:
            path_to_song (string): file name where the song to be provisioned is stored
            metadata (bytearray): bytes containing metadata information
        """
        self.song = path_to_song
        self.full_song, self.original_song = self.read_song(path_to_song)
        self.metadata = metadata

    def save_secured_song_to_wave(self, file_location):
        """Saves secured song to wave file assuming all the same characteristics as original song
        Args:
            file_location (string): location to store the file including name"""
        protected_wav = wave.open(os.path.abspath(file_location), 'wb')
        protected_wav.setnchannels(self.original_song.getnchannels())
        protected_wav.setsampwidth(self.original_song.getsampwidth())
        protected_wav.setframerate(self.original_song.getframerate())
        protected_wav.writeframes(self.metadata)

        for val in self.full_song:
            protected_wav_val = struct.pack('<h', val)
            protected_wav.writeframesraw(protected_wav_val)

        protected_wav.close()

    def read_song(self, path, metadata_frames=0):
        """Reads a wave file
        Args:
            path (string): path to song
            metadata_frames (int): if not 0 disregard this number of frames as metadata
        Returns:
            vals (array): integer array of decoded values
            song (Wave Object): wave object associated with entered song
        """
        song = wave.open(os.path.abspath(path), 'r')
        if metadata_frames:
            song.readframes(metadata_frames)  # skip the metadata frames when assigning vals
        vals = np.frombuffer(song.readframes(song.getnframes()), dtype=np.int16)
        song.close()
        return vals, song


def create_metadata(regions, user, user_secret_location, region_info):
    """Returns a byte string formatted as follows:
    METADATA_LENGTH(1B)/ownerID(1B)/REGION_LEN(1B)/USER_LEN(1B)/REGIONID1(1B)/REGIONID2 (1B)/.../opt. parity
    Args:
        regions (list): list of regions to provision song for
        user (string): user name for owner of the song
        user_secret_location (string): path to user secrets file
        region_info (dict): mapping of regions provided by region_information.json
    Returns:
        metadata (bytes): bytes of encoded metadata
    Example:
        >>create_metadata(['USA', 'Canada'], 'user1', 'user_secrets.json', {'USA': 1, 'Canada':2})
        'x06/x00/x01/x00/x01/x02'
    """
    user_secrets = json.load(open(os.path.abspath(user_secret_location)))

    #user needs to be hashed before it can be mapped in user_secrets
    user = hashlib.sha256(user.encode()).hexdigest()

    # note: metadata must be an even length since each sample is 2B long
    # and ARM processors require memory accesses to be aligned to the type size
    metadata = struct.pack(
        '=3B{regions_length}s{regions_len_2}s'.format(regions_length=len(regions), regions_len_2=len(regions) % 2),
        int(user_secrets[user]['id']), len(regions), 0,
        bytes([region_info[str(r)] for r in regions]),
        b'\x00' if len(regions) % 2 else b'')
    if(len(metadata)%2==1):
        #odd so more needs to be packed on

    return bytes([len(metadata) + 1]) + metadata


def main():
    parser = ArgumentParser(description='main interface to protect songs')
    parser.add_argument('--region-list', nargs='+', help='List of regions song can be played in', required=True)
    parser.add_argument('--region-secrets-path', help='File location for the region secrets file',
                        required=True)
    parser.add_argument('--outfile', help='path to save the protected song', required=True)
    parser.add_argument('--infile', help='path to unprotected song', required=True)
    parser.add_argument('--owner', help='owner of song', required=True)
    parser.add_argument('--user-secrets-path', help='File location for the user secrets file', required=True)
    args = parser.parse_args()

    regions = json.load(open(os.path.abspath(args.region_secrets_path)))
    try:
        metadata = create_metadata(args.region_list, args.owner, args.user_secrets_path, regions)
    except ValueError:
        raise ValueError('Ensure all user IDs are integers and all regions are in the provided region_information.json')
    protected_song = ProtectedSong(args.infile, metadata)
    protected_song.save_secured_song_to_wave(args.outfile)


if __name__ == '__main__':
    main()
