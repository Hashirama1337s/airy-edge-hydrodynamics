# Sealed-test records for Paper II: hashes

For each file: the SHA-256 recorded in the seal file at sealing, whether the lab original at assembly time still
matches it, and the SHA-256 of the copy in this deposit. "redacted = yes" means the deposited copy differs from
the lab original only by the replacement of lab-machine paths with <lab>/, <home>/ or <private folder>/, of a
personal name with [owner], and of approximate times written with a trailing x (or a leading ~) by an explicit
minute range (or "about"). A reader can check a redacted copy only against its own listed hash, not against
the seal. The seal files themselves are in seal-files/ (prefixed with their folder name). Scorers that read lab
paths are run from code/ (path-replaced copies); the copies here are the sealed originals.

| test | file | seal file | sealed sha256 | original now matches | deposited copy sha256 | redacted |
|---|---|---|---|---|---|---|
| DYN1 | BAR-DYN1.md | DYN1/SEAL-DYN1.sha256 | 38d2902058faae46... | yes | 38d2902058faae46549dd6cb3e642f9727fc9a777820a8059998850827dbf418 | no |
| DYN1 | verdict_DYN1.py | DYN1/SEAL-DYN1.sha256 | 39d5bdde5de90371... | yes | 7eb7213b63bff42971b31ded6f01a0651776e8fef4ca26ec308c3aea8bd60408 | yes |
| DYN1 | ADDENDUM-DYN1.md | DYN1/SEAL-DYN1.sha256 | bf374e6bdb44ce0b... | yes | 05abf9fed328b85d00063a552c4ba6a611f60692bf0a8006bd1315130e0bb4b5 | yes |
| DYN1 | verdict-DYN1.txt | DYN1/SEAL-DYN1.sha256 | af43c364a3d6e85a... | yes | af43c364a3d6e85a36d820e28165872e0e6e15ca081aff528ed70c53c2301205 | no |
| DYN1 | blind/RESULT.json | DYN1/SEAL-DYN1.sha256 | 0df73d558653e2bd... | yes | 0df73d558653e2bd513c78940bd592d51aedd18c8e42c96537a9afd005c862c5 | no |
| DYN1 | blind/RESULT.md | DYN1/SEAL-DYN1.sha256 | 4887a31742b6c94a... | yes | 4887a31742b6c94a8f639c491a0a2a325ebba0de5e638c4be790db5861cf43cd | no |
| DYN1b | BAR-DYN1b.md | DYN1b/SEAL-DYN1b.sha256 | 67df857e9dae69b0... | yes | 67df857e9dae69b0b81c42c8e7af1612f818c05cf1dcac4928ca9206e0a986db | no |
| DYN1b | verdict_DYN1b.py | DYN1b/SEAL-DYN1b.sha256 | 505c95f7478734c2... | yes | ffda2f569d1f402db3e9f553434001953fffeb0457d7c05e166a3679a867957a | yes |
| DYN1b | predict_DYN1b.py | DYN1b/SEAL-DYN1b.sha256 | 8b218c573c7e7f01... | yes | 367b47ee82df85b0aab6f4ff32f29d323de915afde69a699ea59d8e5759a83c4 | yes |
| DYN1b | PRED-DYN1b.json | DYN1b/SEAL-DYN1b.sha256 | 3e2019abfe7f1692... | yes | 3e2019abfe7f1692f9a286e05b9daf1240b42270df5ee6392323e3a89075780f | no |
| DYN1b | AMENDMENT-DYN1b.md | DYN1b/SEAL-DYN1b.sha256 | 77a20d37aafd074b... | yes | 77a20d37aafd074b51508974512468cb8c1ede1eae5a8483bfa3c94a7d66169e | no |
| DYN1b | PRED-DYN1b-rivalB.json | DYN1b/SEAL-DYN1b.sha256 | d588ee201a146129... | yes | d588ee201a14612947c7ad1048c340f484ea0e421161d6b0e27b95749b8e2e33 | no |
| DYN1b | backtest_and_rival.py | DYN1b/SEAL-DYN1b.sha256 | 045a61734ec7e478... | yes | 8bdd612ee052acf865489897235324b8cf24cd89864b8463bc5e7db94cf0a972 | yes |
| DYN1b | backtest_and_rival.txt | DYN1b/SEAL-DYN1b.sha256 | a69e4af90393e6ce... | yes | a69e4af90393e6ce545fc03415a957704be546f38de3d55a8e21272445b6b5ce | no |
| DYN1b | DYN1b/verdict-DYN1b.txt | DYN1b/SEAL-DYN1b.sha256 | 98734da488cba53a... | yes | 98734da488cba53a1648592689268c94c0706087a99a56489a21b0169924601b | no |
| DYN1b | DYN1b/blind/RESULT.json | DYN1b/SEAL-DYN1b.sha256 | 430c63bd4cd42c0f... | yes | 430c63bd4cd42c0fd0dc1d84be5f60e90521e7af2be146f67d399b428f090f5b | no |
| DYN1b | DYN1b/blind/RESULT.md | DYN1b/SEAL-DYN1b.sha256 | d979726c306a6d52... | yes | d979726c306a6d52b12814983c32a4a95e88f44cc0f77fe046acd9f0f3685a84 | no |
| THEORY | BAR-THEORY.md | THEORY-TEST/SEAL-THEORY-TEST.sha256 | 3ad717e85c860483... | yes | 3ad717e85c8604832d0b1023ae188a16c9fed83c1df84dc288492a48823feff3 | no |
| THEORY | verdict_THEORY.py | THEORY-TEST/SEAL-THEORY-TEST.sha256 | 17e0f6267a81d974... | yes | 7dc31456134f7cbe97a3852b6938a4f262ba03671eb910db68e5ee04266849d9 | yes |
| THEORY | PRED-THEORY.json | THEORY-TEST/SEAL-THEORY-TEST.sha256 | ab758de0cd198091... | yes | ab758de0cd198091c321aeacc04b1643d239f306290e0c8cc62484e90e8913bb | no |
| THEORY | AMENDMENT-THEORY.md | THEORY-TEST/SEAL-THEORY-TEST.sha256 | 3a4dbc3b94c7a02c... | yes | 3a4dbc3b94c7a02ca75cf420d0d8a37c2ad480f5b36ec9d80df6850e870976d1 | no |
| THEORY | verdict_THEORY_amended.py | THEORY-TEST/SEAL-THEORY-TEST.sha256 | 5f14286c1af24a32... | yes | abfc7a42ab58650e2a4a3982be76148bd096ee1b0136ce501d616b36ce7282af | yes |
| THEORY | T4prime_reference.txt | THEORY-TEST/SEAL-THEORY-TEST.sha256 | ada509d6a41d06ba... | yes | ada509d6a41d06ba3084426eb19a8cfc00645e25c7778949d69f5b26a3f420ff | no |
| THEORY | THEORY-TEST/verdict-THEORY.txt | THEORY-TEST/SEAL-THEORY-TEST.sha256 | 425f0c1115efaec0... | yes | 425f0c1115efaec010e044e6cd3e03df7b23e3e94e4c82f2885b249f061fdd39 | no |
| THEORY | PRED-THEORY.json | theory/SEAL-THEORY.sha256 | ab758de0cd198091... | yes | ab758de0cd198091c321aeacc04b1643d239f306290e0c8cc62484e90e8913bb | no |
| RC | BAR-RC.md | RC/SEAL-RC.sha256 | 117a0f7934a118ba... | yes | d56cf91785c534aec0ed1e87d6241bf06124aef9547e9abb70fd0ec87c67f55e | yes |
| RC | verdict_RC.py | RC/SEAL-RC-verdict.sha256 | e8a73fa5b4a40d13... | yes | e8a73fa5b4a40d138743830f54d5b77b43ade7952c0016d28c3ed9f498cd4b33 | no |
| RC | verdict-RC.txt | RC/SEAL-RC-verdict.sha256 | 2bc01d094ec128a4... | yes | 2bc01d094ec128a4417ed5c4fc3843fca33e5ad4828a3e0dbf7cb74ba3081431 | no |
| RC | RESULT.json | RC/SEAL-RC-verdict.sha256 | 9fb6b01b5e9e2dc8... | yes | 9fb6b01b5e9e2dc80a857c3f43e93b1891850506389f74b3f27c6a7038e494a7 | no |
| RC | RESULT.md | RC/SEAL-RC-verdict.sha256 | 943c7f010f0c928b... | yes | 99be8eea4903773b726d822428e3f502b7565821dd7dcce77ec07c9c0e63d419 | yes |
| RC2 | BAR-RC2.md | RC2/SEAL-RC2.sha256 | 02e63c4dda442787... | yes | 0c122595092573636a35e9ca6b6425c11e3a044dec3f5ff36c679747221a9004 | yes |
| RC2 | verdict_RC2.py | RC2/SEAL-RC2.sha256 | 7939a815680ea862... | yes | 7939a815680ea862291f7234db4661c11e680862c1bf988536f584a2a652f135 | no |
| RC2 | RC2/ADDENDUM-RC2.md | RC2/SEAL-RC2.sha256 | a6f133f7b8ef21b0... | yes | 1d26e1866e9e1872208db583d317efc1cc077b763f3bdc9a5a42527c2c12d527 | yes |
| RC2 | verdict_RC2_fix1.py | RC2/SEAL-RC2-verdict.sha256 | 8ce54858b4356e5e... | yes | 8ce54858b4356e5e0c2b6a98cc5ca72c7ab53482900684de2a607ad0327348e3 | no |
| RC2 | verdict-RC2.txt | RC2/SEAL-RC2-verdict.sha256 | 41aa8c4e7372fe29... | yes | 41aa8c4e7372fe2928af621c742c40bd023638611ab1ddcf35d7205697769d0a | no |
| RC2 | blind/RESULT.json | RC2/SEAL-RC2-verdict.sha256 | 020bc3580d3b03f5... | yes | 020bc3580d3b03f5901b8d8a60e56df1f19eb282ca238382f71c5694999ddf62 | no |
| RC2 | blind/RESULT.md | RC2/SEAL-RC2-verdict.sha256 | ae715b6a1906efdc... | yes | ae715b6a1906efdc6ba8ef08dde424a7164ac2f6e0b22d21c5ef74c3e8639738 | no |
| RC3 | BAR-RC3.md | RC3/SEAL-RC3.sha256 | 6eed4eff5293a3bb... | yes | c9cf629829c60ed7efe4a9e93e91463b9bd005d210df1831caf8b8621ae70aee | yes |
| RC3 | verdict_RC3.py | RC3/SEAL-RC3.sha256 | bacee34cea4fe561... | yes | bacee34cea4fe56192e175535fa79014a8a947a54d7a3e4225060a86fb1847bd | no |
| RC3 | RC3/verdict-RC3.txt | RC3/SEAL-RC3-verdict.sha256 | a6e0d446acce3719... | yes | a6e0d446acce371939e264e6736bd000b2dfb2739c66e786ee7b8e005b8ce4aa | no |
| RC3 | RC3/blind/RESULT.json | RC3/SEAL-RC3-verdict.sha256 | ada624750b4fb62f... | yes | ada624750b4fb62f70de6216944ba6ac2e0f0d581988cf08a54bd0f658c78934 | no |
| RC3 | RC3/blind/RESULT.md | RC3/SEAL-RC3-verdict.sha256 | eb6d80dd83bb7c50... | yes | eb6d80dd83bb7c50ba0d9a29734d7e1496dedc7ab9a3f3844e338630035b4dce | no |
| RC3R | BAR-RC3R.md | RC3/SEAL-RC3R.sha256 | c87b473b37cf02f3... | yes | c87b473b37cf02f38f5c09647d4566a657949afdbfd9b44cc1b61b1b4406cde2 | no |
| RC3R | verdict_RC3R.py | RC3/SEAL-RC3R.sha256 | 56186ef09d117030... | yes | 56186ef09d11703010441c815fe265c97e0e38f0907a6a83fbed2a7c2f73707d | no |
| RC3R | verdict-RC3R.txt | RC3/SEAL-RC3R-verdict.sha256 | caa4bbfcd1be29df... | yes | caa4bbfcd1be29df90a121756c7d5ab1602e8a0434c91abff44af4258dd377ae | no |
| RC3R | blind/RESULT-R.json | RC3/SEAL-RC3R-verdict.sha256 | 8821a0612c509c30... | yes | 8821a0612c509c30517f62a8b0afdbee5bbd0d7183f217a3ac1c8a3ded497a13 | no |
| RC3R | blind/RESULT-R.md | RC3/SEAL-RC3R-verdict.sha256 | df6e4e0ee6f2b997... | yes | df6e4e0ee6f2b99795162deea15b00bd0acad86412326cebefb11bcc5cff4d50 | no |
| DYN2 | BAR-DYN2.md | DYN2/SEAL-DYN2.sha256 | 2b0ae6013408a8ec... | yes | 2b0ae6013408a8ec5189754908e9a95628555aebb9804db3e2b26228811d9dd9 | no |
| DYN2 | verdict_DYN2.py | DYN2/SEAL-DYN2.sha256 | 3a2c83eaf1ac521c... | yes | beff2f52fb3df7ce6720cbf6de6d470a6ec8e60a214abe47362f1907f2dbd62b | yes |
| DYN2 | PRED-DYN.json | DYN2/SEAL-DYN2.sha256 | 9e3744e406975c6b... | yes | 9e3744e406975c6b94c788d071503bfc7db1052e5a4d056fa1b24904263e31cc | no |
| DYN2 | ADDENDUM-DYN2.md | DYN2/SEAL-DYN2.sha256 | 09e960385702bfc6... | yes | 09e960385702bfc6fde66698dfcce80047c40a0dae106da7a6ccd1932bffd748 | no |
| DYN2 | verdict-DYN2.txt | DYN2/SEAL-DYN2.sha256 | 3585cdeb1565223b... | yes | 3585cdeb1565223bb504e1010177bfe4577e7ba35225586ccd2bb0e96490c9ac | no |
| DYN2 | blind/RESULT.json | DYN2/SEAL-DYN2.sha256 | a80afaa71cf335bc... | yes | a80afaa71cf335bc1598f928c738e9a9a5fc3a6498703c42dc0297d951e1c44b | no |
| DYN2 | blind/RESULT.md | DYN2/SEAL-DYN2.sha256 | e72dfe9311d2ac1f... | yes | aa707b580e003caca57a1a49ff6434bc12f5a53ceafd2713ef7a73b63df539f1 | yes |
| DYN3 | BAR-DYN3.md | DYN3/SEAL-DYN3.sha256 | fbf83ee9ca816513... | yes | fbf83ee9ca81651347b8ab418bb56f07595bcb7eddb4034721ca2c1bf2cac798 | no |
| DYN3 | verdict_DYN3.py | DYN3/SEAL-DYN3.sha256 | 59446b001277560f... | yes | 4b43c315e3bad287f545cb1d08f5e67a6551cef8ba0476034c702c65000ebda1 | yes |
| DYN3 | PRED-SOUND.json | DYN3/SEAL-DYN3.sha256 | 1e85f6c049f8bf2d... | yes | ef0373467851071115d86a6f6ffd4b13fb7e3e50fb254987d131210b5d7c7dcb | yes |
| DYN3 | ADDENDUM-DYN3.md | DYN3/SEAL-DYN3.sha256 | 61e6ac40045dd9f1... | yes | 154c8a8c578acc79fe877a122a1c5b2cac535b2b26f840cc8453b279b055a6a2 | yes |
| DYN3 | verdict-DYN3.txt | DYN3/SEAL-DYN3.sha256 | 19510f79cf54810e... | yes | 19510f79cf54810e7099c98d2bc6b1f85bf78fff4266f4c35c7e9ea9e1c67e75 | no |
| DYN3 | blind/RESULT.json | DYN3/SEAL-DYN3.sha256 | 3ba3e343a6b15377... | yes | 3ba3e343a6b15377ee808b99b3f3588f715aa9cce54eccedb5e6c869650e2570 | no |
| DYN3 | blind/RESULT.md | DYN3/SEAL-DYN3.sha256 | bd6f13e54d92dbf2... | yes | 6ccede2c825eb6a55758b03f8d956a04d8a25c7c746296437c72e42b23bcd748 | yes |
| SHEAR | BAR-SHEAR.md | zeta-k5/SEAL-ROUND3.sha256 | 3c36dbb65f1d0a6b... | yes | 3c36dbb65f1d0a6b8e6791b80483659d37ab8006513d67849839d3ab2ef19083 | no |
| SHEAR | AMENDMENT-A1-SHEAR.md | zeta-k5/SEAL-ROUND3.sha256 | 0ef67b6d9f109ac9... | yes | 0ef67b6d9f109ac97cce64ddea613d551fe1e55ac84e07325dfa80fc20a5afb2 | no |
| SHEAR | verdict_shear.py | zeta-k5/SEAL-ROUND3.sha256 | 7500592fbd6c74db... | yes | c6f825d2f307fe7d3c0be477535f3b4a52239c993d3020cc487a9cb2317dc4a7 | yes |
| SHEAR | verdict-SHEAR.txt | zeta-k5/SEAL-ROUND3.sha256 | 15fe2a5da77676de... | yes | 15fe2a5da77676de6ddeccb7fbfc1942edd44c73509e3811434b14140f59504d | no |
| SHEAR | shear/RESULT.json | zeta-k5/SEAL-ROUND3.sha256 | addaa0b4587f88be... | yes | addaa0b4587f88bebf9b66f456c51c9f94ee9b775eb37b3a86b27a675afcf9c6 | no |
| SHEAR | shearB/RESULT.json | zeta-k5/SEAL-ROUND3.sha256 | a8e256ba959f3302... | yes | a8e256ba959f330214efffb81d565befbac24f0cd47437a2b137a3809b2c44c1 | no |
