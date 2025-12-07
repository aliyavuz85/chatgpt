const { useEffect, useState } = React;

function App() {
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(1);
  const [documents, setDocuments] = useState([]);
  const [total, setTotal] = useState(0);
  const [selectedDoc, setSelectedDoc] = useState(null);

  const pageSize = 100;

  useEffect(() => {
    fetchDocuments();
  }, [page]);

  const fetchDocuments = async () => {
    const url = new URL("/documents", window.API_BASE || window.location.origin);
    if (query) url.searchParams.set("q", query);
    url.searchParams.set("page", page);
    url.searchParams.set("page_size", pageSize);

    const res = await fetch(url);
    const data = await res.json();
    setDocuments(data.items);
    setTotal(data.total);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    fetchDocuments();
  };

  const totalPages = Math.max(1, Math.ceil(total / pageSize));

  const openDoc = (docId) => {
    const url = `${window.API_BASE || ''}/documents/${docId}/file`;
    window.open(url, '_blank');
  };

  const showContent = async (docId) => {
    const res = await fetch(`${window.API_BASE || ''}/documents/${docId}/content`);
    const data = await res.json();
    setSelectedDoc(data);
  };

  return (
    React.createElement('div', null,
      React.createElement('header', null,
        React.createElement('h1', null, 'Evrak Takip'),
        React.createElement('div', null, new Date().toLocaleDateString('tr-TR'))
      ),
      React.createElement('div', { className: 'container' },
        React.createElement('form', { className: 'search-row', onSubmit: handleSearch },
          React.createElement('input', {
            placeholder: 'Konu veya içerik ara...',
            value: query,
            onChange: (e) => setQuery(e.target.value),
          }),
          React.createElement('button', { type: 'submit' }, 'Ara')
        ),
        React.createElement('div', { className: 'table-wrapper' },
          React.createElement('table', null,
            React.createElement('thead', null,
              React.createElement('tr', null,
                ['Tarih', 'Konu', 'İçerik (250 karakter)', 'Evrak No', 'Aç'].map((header) =>
                  React.createElement('th', { key: header }, header)
                )
              )
            ),
            React.createElement('tbody', null,
              documents.map((doc) =>
                React.createElement('tr', { key: doc.id },
                  React.createElement('td', null, doc.doc_date || '-'),
                  React.createElement('td', null,
                    React.createElement('a', {
                      href: '#',
                      onClick: (e) => {
                        e.preventDefault();
                        showContent(doc.id);
                      },
                    }, doc.topic)
                  ),
                  React.createElement('td', null, doc.content.slice(0, 250)),
                  React.createElement('td', null, doc.doc_number || '-'),
                  React.createElement('td', null,
                    React.createElement('button', { onClick: () => openDoc(doc.id) }, 'Aç')
                  ),
                )
              )
            )
          )
        ),
        React.createElement('div', { className: 'pagination' },
          Array.from({ length: totalPages }).map((_, idx) => (
            React.createElement('button', {
              key: idx,
              onClick: () => setPage(idx + 1),
              style: { fontWeight: page === idx + 1 ? 'bold' : 'normal' },
            }, `Sayfa ${idx + 1}`)
          ))
        ),
        selectedDoc && React.createElement('div', { className: 'details-panel' },
          React.createElement('h3', null, selectedDoc.topic),
          React.createElement('p', null, `Evrak No: ${selectedDoc.doc_number || '-'}`),
          React.createElement('p', null, `Tarih: ${selectedDoc.doc_date || '-'}`),
          React.createElement('pre', null, selectedDoc.content)
        )
      )
    )
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App));
