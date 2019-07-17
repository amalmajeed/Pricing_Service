from models.user.user import User
import models.user.errors as UserErrors
from models.user.decorators import requires_login, requires_admin


"""

Doing the above steps in a python package can eliminate the hassle of re defining what all to import in every file that inherits from a python
package. Instead python simply inherits from the dunder init file of a package by simply importing from the package anyways.

"""