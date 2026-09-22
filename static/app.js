const endpoints = {
  produto: '/produtos',
  cliente: '/clientes',
  venda: '/vendas',
  categoria: '/categorias',
  fornecedor: '/fornecedores'
};

const labels = {
  dashboard: 'Visão geral',
  produtos: 'Inventário',
  clientes: 'Clientes',
  fornecedores: 'Fornecedores',
  vendas: 'Vendas',
  cadastros: 'Cadastros'
};

const $ = selector => document.querySelector(selector);

function showToast(message, error = false) {
  const toast = $('#toast');
  toast.textContent = message;
  toast.style.background = error ? '#b64d3d' : 'var(--navy)';
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3000);
}

function goTo(view) {
  document.querySelectorAll('.page').forEach(page => page.classList.add('hidden'));
  $(`#view-${view}`).classList.remove('hidden');

  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.toggle('active', item.dataset.view === view);
  });

  $('#breadcrumb-label').textContent = labels[view];

  if (window.innerWidth < 701) {
    $('#sidebar').classList.remove('open');
  }
}

function applyTheme(theme) {
  const isDark = theme === 'dark';
  document.body.classList.toggle('dark-theme', isDark);

  const toggleButton = document.getElementById('theme-toggle');
  if (toggleButton) {
    toggleButton.textContent = isDark ? '☀️' : '🌙';
    toggleButton.setAttribute('aria-label', isDark ? 'Ativar modo claro' : 'Ativar modo escuro');
    toggleButton.title = isDark ? 'Modo claro' : 'Modo escuro';
  }
}

function toggleTheme() {
  const current = localStorage.getItem('motora-theme') === 'dark' ? 'light' : 'dark';
  localStorage.setItem('motora-theme', current);
  applyTheme(current);
}

const savedTheme = localStorage.getItem('motora-theme') || 'light';
applyTheme(savedTheme);

const themeToggleButton = document.getElementById('theme-toggle');
if (themeToggleButton) {
  themeToggleButton.addEventListener('click', toggleTheme);
}

const formFields = {
  produto: [
    { name: 'nome', label: 'Nome do produto', type: 'text', required: true },
    { name: 'preco', label: 'Preço', type: 'number', required: true },
    { name: 'estoque', label: 'Estoque', type: 'number', required: true },
    { name: 'descricao', label: 'Descrição', type: 'text', required: false },
    { name: 'id_categoria', label: 'ID da categoria', type: 'number', required: true },
    { name: 'id_fornecedor', label: 'ID do fornecedor', type: 'number', required: true },
    { name: 'codigo_de_barra', label: 'Código de barras', type: 'text', required: true }
  ],
  cliente: [
    { name: 'nome', label: 'Nome completo', type: 'text', required: true },
    { name: 'cpf', label: 'CPF', type: 'text', required: true, maxLength: 11 },
    { name: 'telefone', label: 'Telefone', type: 'text', required: false, maxLength: 11 },
    { name: 'email', label: 'E-mail', type: 'email', required: false },
    { name: 'endereco', label: 'Endereço', type: 'text', required: false },
    { name: 'aceite_lgpd', label: 'Aceito os termos da LGPD', type: 'checkbox', required: true }
  ],
  categoria: [
    { name: 'nome', label: 'Nome da categoria', type: 'text', required: true },
    { name: 'descricao', label: 'Descrição', type: 'text', required: true }
  ],
  fornecedor: [
    { name: 'nome', label: 'Nome da empresa', type: 'text', required: true },
    { name: 'cnpj', label: 'CNPJ', type: 'text', required: true, maxLength: 14 },
    { name: 'telefone', label: 'Telefone', type: 'text', required: false, maxLength: 11 },
    { name: 'email', label: 'E-mail', type: 'email', required: false }
  ],
  venda: [
    { name: 'data_venda', label: 'Data da venda', type: 'date', required: true },
    { name: 'valor_total', label: 'Valor total', type: 'number', required: true },
    { name: 'id_cliente', label: 'ID do cliente', type: 'number', required: true }
  ]
};

function openForm(type) {
  document.querySelectorAll('.modal-backdrop').forEach(modal => {
    modal.classList.add('hidden');
    modal.classList.remove('show');
  });

  const modal = document.getElementById(`modal-${type}`);
  if (!modal) return;

  modal.classList.remove('hidden');
  modal.classList.add('show');

  const dateField = modal.querySelector('[name="data_venda"]');
  if (dateField && !dateField.value) {
    dateField.value = new Date().toISOString().slice(0, 10);
  }
}

function parseSelectedProductId(value) {
  if (value === null || value === undefined) return null;

  const text = String(value).trim();
  if (!text) return null;

  const match = text.match(/^\s*(\d+)/);
  if (match) return Number(match[1]);

  const product = Array.isArray(window.produtosCatalog)
    ? window.produtosCatalog.find(item => item.nome && item.nome.toLowerCase() === text.toLowerCase())
    : null;

  return product ? Number(product.id_produto) : null;
}

function getSelectedSaleProduct() {
  const form = document.getElementById('form-venda');
  if (!form) return null;

  const productId = parseSelectedProductId(form.querySelector('[name="id_produto"]')?.value);

  if (productId === null || productId === undefined) return null;

  return Array.isArray(window.produtosCatalog)
    ? window.produtosCatalog.find(item => Number(item.id_produto) === Number(productId))
    : null;
}

function updateSaleTotal() {
  const form = document.getElementById('form-venda');
  if (!form) return;

  const product = getSelectedSaleProduct();
  const quantityField = form.querySelector('[name="quantidade"]');
  const quantity = normalizeNumber(quantityField?.value);
  const totalField = form.querySelector('[name="valor_total"]');

  if (!totalField) return;

  if (product) {
    const stock = Number(product.estoque ?? 0);
    if (quantityField) {
      quantityField.max = String(stock);
      if (stock === 0) {
        quantityField.value = '';
        showToast(`O produto "${product.nome}" está sem estoque disponível.`, true);
      } else if (quantity !== null && quantity > stock) {
        quantityField.value = String(stock);
        showToast(`Quantidade máxima disponível: ${stock}.`, true);
      }
    }
  } else if (quantityField) {
    quantityField.removeAttribute('max');
  }

  const unitValue = product ? Number(product.preco) : null;

  if (unitValue !== null && quantity !== null && quantity > 0) {
    const total = unitValue * quantity;
    totalField.value = total.toFixed(2);
  } else {
    totalField.value = '';
  }
}

function normalizeNumber(value) {
  const cleaned = String(value ?? '').trim();
  return cleaned === '' || cleaned === 'null' ? null : Number(cleaned);
}

function filterTableRows({ selector, countSelector, value }) {
  const query = value.trim().toLowerCase();
  const rows = document.querySelectorAll(selector);

  rows.forEach(row => {
    const text = (row.dataset.name || '').toLowerCase();
    row.style.display = text.includes(query) ? '' : 'none';
  });

  const visibleRows = [...rows].filter(row => row.style.display !== 'none');
  const count = document.querySelector(countSelector);
  if (count) {
    count.textContent = `${visibleRows.length} itens`;
  }
}

function updateProductStockInfo() {
  const stockInfo = document.getElementById('produto-estoque-info');
  const productInput = document.getElementById('produto-estoque-selecionado');
  if (!stockInfo || !productInput) return;

  const selectedValue = productInput.value;
  if (!selectedValue) {
    stockInfo.textContent = 'Selecione um produto para ver o estoque atual.';
    stockInfo.style.color = 'var(--muted)';
    return;
  }

  const parsedId = parseSelectedProductId(selectedValue);
  const product = Array.isArray(window.produtosCatalog)
    ? window.produtosCatalog.find(item => Number(item.id_produto) === Number(parsedId))
    : null;

  if (!product) {
    stockInfo.textContent = 'Produto não encontrado no catálogo.';
    stockInfo.style.color = '#b64d3d';
    return;
  }

  stockInfo.textContent = `Estoque atual: ${product.estoque ?? 0} unidades.`;
  stockInfo.style.color = Number(product.estoque ?? 0) > 0 ? 'var(--green)' : '#b64d3d';
}

async function submitForm(event, type) {
  event.preventDefault();

  const form = event.currentTarget;
  if (!form || form.dataset.type !== type) return;

  const rawData = new FormData(form);
  const payload = {};

  for (const [key, value] of rawData.entries()) {
    if (key === 'aceite_lgpd') {
      payload.aceite_lgpd = value === 'true' || value === 'on' || value === true;
      continue;
    }

    if (value === '') continue;
    payload[key] = value;
  }

  if (type === 'produto') {
    payload.preco = normalizeNumber(payload.preco);
    payload.estoque = normalizeNumber(payload.estoque);
    payload.id_categoria = normalizeNumber(payload.id_categoria);
    payload.id_fornecedor = normalizeNumber(payload.id_fornecedor);

    if (!payload.nome || payload.preco === null || payload.estoque === null || !payload.codigo_de_barra || payload.id_categoria === null || payload.id_fornecedor === null) {
      showToast('Preencha todos os campos obrigatórios do produto.', true);
      return;
    }
  }

  if (type === 'produto-estoque') {
    const produtoExistenteId = parseSelectedProductId(payload.produto_existente_id);
    const quantidadeAdicionar = normalizeNumber(payload.estoque_adicional);
    const produtoExistente = Array.isArray(window.produtosCatalog)
      ? window.produtosCatalog.find(item => Number(item.id_produto) === Number(produtoExistenteId))
      : null;

    if (produtoExistenteId === null || quantidadeAdicionar === null || quantidadeAdicionar <= 0 || !produtoExistente) {
      showToast('Selecione um produto existente e informe a quantidade a adicionar.', true);
      return;
    }

    const novoEstoque = Number(produtoExistente.estoque ?? 0) + quantidadeAdicionar;

    try {
      const response = await fetch(`/produtos/${produtoExistente.id_produto}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ estoque: novoEstoque })
      });

      const result = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(result.erro || 'Erro ao repor estoque');

      showToast('Estoque reposto com sucesso.');
      const modal = document.getElementById('modal-produto-estoque');
      if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('show');
      }
      window.location.reload();
      return;
    } catch (error) {
      showToast(error.message, true);
      return;
    }
  }

  if (type === 'cliente') {
    payload.aceite_lgpd = payload.aceite_lgpd === true;

    if (!payload.nome || !payload.cpf || !payload.aceite_lgpd) {
      showToast('Nome, CPF e aceitação da LGPD são obrigatórios.', true);
      return;
    }
  }

  if (type === 'categoria') {
    if (!payload.nome || !payload.descricao) {
      showToast('Nome e descrição da categoria são obrigatórios.', true);
      return;
    }
  }

  if (type === 'fornecedor') {
    if (!payload.nome || !payload.cnpj) {
      showToast('Nome e CNPJ do fornecedor são obrigatórios.', true);
      return;
    }
  }

  if (type === 'venda') {
    payload.valor_total = normalizeNumber(payload.valor_total);
    payload.id_cliente = normalizeNumber(payload.id_cliente);
    payload.id_produto = parseSelectedProductId(payload.id_produto);
    payload.quantidade = normalizeNumber(payload.quantidade);

    const selectedProduct = Array.isArray(window.produtosCatalog)
      ? window.produtosCatalog.find(item => Number(item.id_produto) === Number(payload.id_produto))
      : null;

    if (selectedProduct) {
      const estoqueDisponivel = Number(selectedProduct.estoque ?? 0);

      if (estoqueDisponivel === 0) {
        showToast(`O produto "${selectedProduct.nome}" está sem estoque disponível.`, true);
        return;
      }

      if (payload.quantidade > estoqueDisponivel) {
        showToast(`Quantidade indisponível. Máximo no estoque: ${estoqueDisponivel}.`, true);
        return;
      }

      payload.preco_unitario = Number(selectedProduct.preco);
      payload.valor_total = Number((payload.preco_unitario * payload.quantidade).toFixed(2));
    }

    if (!payload.data_venda || payload.id_cliente === null || payload.id_produto === null || payload.quantidade === null || payload.quantidade <= 0 || payload.preco_unitario === undefined || payload.preco_unitario === null || payload.valor_total === null) {
      showToast('Data, produto, quantidade e cliente são obrigatórios.', true);
      return;
    }
  }

  try {
    let response;
    let result = {};

    if (type === 'venda') {
      response = await fetch(endpoints[type], {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          data_venda: payload.data_venda,
          valor_total: payload.valor_total,
          id_cliente: payload.id_cliente
        })
      });

      result = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(result.erro || 'Erro ao salvar venda');
      }

      const id_venda = result.id_venda;
      const itemResponse = await fetch('/item_venda', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id_venda,
          id_produto: payload.id_produto,
          quantidade: payload.quantidade,
          preco_unitario: payload.preco_unitario
        })
      });

      const itemResult = await itemResponse.json().catch(() => ({}));

      if (!itemResponse.ok) {
        throw new Error(itemResult.erro || 'Erro ao salvar item da venda');
      }
    } else {
      response = await fetch(endpoints[type], {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      result = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(result.erro || 'Erro ao salvar');
      }
    }

    showToast('Cadastro realizado com sucesso.');
    const modal = document.getElementById(`modal-${type}`);
    if (modal) {
      modal.classList.add('hidden');
      modal.classList.remove('show');
    }
    window.location.reload();
  } catch (error) {
    showToast(error.message, true);
  }
}

document.addEventListener('click', event => {
  const nav = event.target.closest('[data-view]');
  if (nav) goTo(nav.dataset.view);

  const formButton = event.target.closest('[data-open-form]');
  if (formButton) {
    const type = formButton.dataset.openForm;
    openForm(type);

    if (type === 'produto-estoque') {
      const productId = formButton.dataset.productId;
      const productField = document.getElementById('produto-estoque-selecionado');
      if (productField) {
        productField.value = productId ? String(productId) : '';
        updateProductStockInfo();
      }
    }
  }

  const closeButton = event.target.closest('[data-close]');
  if (closeButton) {
    const modal = document.getElementById(`modal-${closeButton.dataset.close}`);
    if (modal) {
      modal.classList.add('hidden');
      modal.classList.remove('show');
    }
  }
});

const formTypes = ['produto', 'produto-estoque', 'cliente', 'categoria', 'fornecedor', 'venda'];

formTypes.forEach(type => {
  const form = document.getElementById(`form-${type}`);
  if (form) {
    form.addEventListener('submit', event => submitForm(event, type));

    if (type === 'venda') {
      const productField = form.querySelector('[name="id_produto"]');
      const quantityField = form.querySelector('[name="quantidade"]');

      [productField, quantityField].forEach(field => {
        if (field) {
          field.addEventListener('input', updateSaleTotal);
          field.addEventListener('change', updateSaleTotal);
        }
      });

      if (productField) {
        productField.addEventListener('change', updateSaleTotal);
      }
    }
  }
});

const productStockInput = document.getElementById('produto-estoque-selecionado');
if (productStockInput) {
  productStockInput.addEventListener('input', updateProductStockInfo);
  productStockInput.addEventListener('change', updateProductStockInfo);
}

const menuButton = $('#menu-button');
if (menuButton) {
  menuButton.addEventListener('click', () => {
    $('#sidebar').classList.toggle('open');
  });
}

function getSelectedCategoryIds() {
  return [...document.querySelectorAll('.category-checkbox')]
    .filter(checkbox => checkbox.checked)
    .map(checkbox => Number(checkbox.value));
}

function applyProductFilters() {
  const rows = document.querySelectorAll('#products-table [data-row]');
  const searchValue = ($('#product-search')?.value || '').trim().toLowerCase();
  const selectedCategories = getSelectedCategoryIds();

  rows.forEach(row => {
    const matchesSearch = (row.dataset.name || '').toLowerCase().includes(searchValue);
    const categoryId = Number(row.dataset.categoryId);
    const matchesCategory = selectedCategories.length === 0 ? false : selectedCategories.includes(categoryId);
    row.style.display = matchesSearch && matchesCategory ? '' : 'none';
  });

  const visibleRows = [...rows].filter(row => row.style.display !== 'none');
  const count = document.querySelector('#product-count');
  if (count) {
    count.textContent = `${visibleRows.length} itens`;
  }
}

const productSearch = $('#product-search');
if (productSearch) {
  productSearch.addEventListener('input', applyProductFilters);
}

const categoryFilterToggle = $('#category-filter-toggle');
const categoryFilterPanel = $('#category-filter-panel');
if (categoryFilterToggle && categoryFilterPanel) {
  categoryFilterToggle.addEventListener('click', () => {
    categoryFilterPanel.classList.toggle('hidden');
  });
}

const selectAllCategories = $('#select-all-categories');
if (selectAllCategories) {
  selectAllCategories.addEventListener('click', () => {
    const checkboxes = document.querySelectorAll('.category-checkbox');
    const shouldCheck = [...checkboxes].some(checkbox => !checkbox.checked);

    checkboxes.forEach(checkbox => {
      checkbox.checked = shouldCheck;
    });

    applyProductFilters();
  });
}

document.querySelectorAll('.category-checkbox').forEach(checkbox => {
  checkbox.addEventListener('change', applyProductFilters);
});

const clientSearch = $('#client-search');
if (clientSearch) {
  clientSearch.addEventListener('input', event => {
    filterTableRows({
      selector: '#clients-table [data-row]',
      countSelector: '#client-count',
      value: event.target.value
    });
  });
}

const supplierSearch = $('#supplier-search');
if (supplierSearch) {
  supplierSearch.addEventListener('input', event => {
    filterTableRows({
      selector: '#supplier-table [data-row]',
      countSelector: '#supplier-count',
      value: event.target.value
    });
  });
}

const salesSearch = $('#sales-search');
if (salesSearch) {
  salesSearch.addEventListener('input', event => {
    filterTableRows({
      selector: '#sales-table [data-row]',
      countSelector: '#sales-count',
      value: event.target.value
    });
  });
}

const todayLabel = $('#today-label');
if (todayLabel) {
  todayLabel.textContent = new Date().toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  });
}