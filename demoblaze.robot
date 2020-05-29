*** Settings ***
Library    demoblaze  WITH NAME  db

*** Keywords ***
Add Product To Cart
    [Arguments]  ${id}=1
    db.Open Main Page
    db.Open Product  id=${id}
    db.Add Current Product To Cart

*** Test Cases ***
Add one product to cart
    [Tags]  add
    [Setup]    db.Clear Cart
    Add Product To Cart  id=1
    db.Open Cart
    db.Verify Product In Cart  count=1  name=Samsung galaxy s6
    [Teardown]    db.Clear Cart

Delete product from cart
    [Tags]  delete
    [Setup]    Add Product To Cart  id=1
    db.Open Cart
    db.Delete Product From Cart
    ${products}=  db.Get Number Of Products In Cart
    Should Be Equal    ${products}  ${0}
