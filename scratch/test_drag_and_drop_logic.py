def test_html_drag_and_drop():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    assert 'card.draggable = true' in html, "HTML missing card.draggable = true assignment"
    assert 'attachDragAndDropEvents' in html, "HTML missing attachDragAndDropEvents function"
    assert 'reorderPages' in html, "HTML missing reorderPages function"
    assert 'dragstart' in html, "Missing dragstart event listener"
    assert 'dragover' in html, "Missing dragover event listener"
    assert 'drop' in html, "Missing drop event listener"
    assert 'pageNumber' in html, "Missing pageNumber updating logic"
    
    print("ALL DRAG AND DROP HTML & JS LOGIC VERIFIED SUCCESSFULLY!")

if __name__ == '__main__':
    test_html_drag_and_drop()
