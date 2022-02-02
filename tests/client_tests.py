#  Copyright (c) 2022. Kodexa Inc
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from kodexa import KodexaClient


def test_basic_client():
    kodexa_client = KodexaClient('https://dev2.kodexa.com', 'f30c94abcd25434a9703d827ebdcbb7f')
    print(kodexa_client.get_platform())
    print(kodexa_client.organizations.list())

