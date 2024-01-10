from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class LicenseProvider (SpireObject) :
    """
    A class representing a license provider.

    Attributes:
        None

    Methods:
        Register: Registers a user with a license code.

    """
    @staticmethod

    def Register(userName:str,code:str):
        """
        Registers a user with a license code.

        Args:
            userName: A string representing the user's name.
            code: A string representing the license code.

        Returns:
            None

        """
        userNamePtr = StrToPtr(userName)
        codePtr = StrToPtr(code)
        GetDllLibDoc().LicenseProvider_Register.argtypes=[c_char_p,c_char_p]
        CallCFunction(GetDllLibDoc().LicenseProvider_Register,userNamePtr,codePtr)

