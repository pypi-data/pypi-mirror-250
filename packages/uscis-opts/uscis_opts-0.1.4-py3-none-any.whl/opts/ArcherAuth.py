"""
ArcherAPI.ArcherAuth

This module provides an ArcherAuth class, whose instantiated objects will hold
signed credentials to the specified Archer instance.

In addition to signed credentials, we store the Archer instance url and session
object that will be used by the ArcherServerClient class to make requests.
"""
import re
import requests
from opts.ArcherServerClient import ArcherServerClient
from opts.SigningError import SigningError

class ArcherAuth:
  def __init__(self, ins: str,
               usr: str, pwd: str,
               url: str, dom = '') -> None:
    """Instantiate an ArcherAuth object.
    Positional arguments:
    1) ins: Name of Archer instance. (e.g.'Prod', 'Test', etc.)
    2) usr: Username of account to authenticate and request against.
    3) pwd: Password of account to authenticate and request against.
    4) url: Base url of Archer instance. (e.g 'https://optstest.uscis.dhs.gov')
    Keyword arguments:
    1) dom: Userdomain. Almost always blank.
    """
    self.ins = ins
    self.dom = dom
    self.usr = usr
    self.pwd = pwd
    self.base_url = re.search('(https:\/\/[^\/]*)', url).group(1)
    self.token = None
    self.authenticated = False
    self.session = requests.Session()
    self.session.headers.update(
      {'Accept': 'application/json',
       'Content-Type': 'application/json'}
    )
    #TESTING ONLY!!!
    # self.session.verify = False
    #TESTING ONLY!!!

  def login(self) -> None:
    """Login to Archer instance with credentials provided during instantiation.
    """
    if not self.authenticated:
      response = self.session.post(
        f'{self.base_url}/platformapi/core/security/login',
        json = {'InstanceName': self.ins,
                'Username': self.usr,
                'UserDomain': self.dom,
                'Password': self.pwd}
      )
    
      if (response.status_code != 200
          or not response.json()['IsSuccessful']):
        # Login was unsucessful.
        raise SigningError(response.status_code, response.text)
    
      self.token = response.json()['RequestedObject']['SessionToken']
      self.session.headers.update(
        {'Authorization': f'Archer session-id={self.token}'}
      )
      self.authenticated = True

  def logout(self) -> None:
    """Logout of Archer instance with signed credentials recieved during login.
    """
    if self.authenticated:
      response = self.session.post(
        f'{self.base_url}/platformapi/core/security/logout',
        json = {'Value': self.token}
      )

      if (response.status_code != 200
          or not response.json()['IsSuccessful']):
        # Logout was unsucessful.
        raise SigningError(response.status_code, response.text)
    
      self.session.close() # Not sure this is necessary.
      self.authenticated = False

  def __enter__(self) -> ArcherServerClient:
    self.login()
    return ArcherServerClient(self)

  def __exit__(self, *args, **kwargs) -> bool:
    self.logout()
    return False