#pragma once 

#include <stddef.h>
#include <type_traits>

namespace order_statistic_tree {

    template <typename T> 
    struct WeightBalancedTree {

        using DataType = T; 

        struct Node {
            T value; 
            size_t size; 
            Node *son[2]; 
            Node *parent; 
        }; 

        Node *root; 

    }; 

    template <typename ...Args> 
    using WBT = WeightBalancedTree<Args...>; 

    template <typename T>
    WeightBalancedTree<T> *default_tree() {
        auto tree = new WeightBalancedTree<T>; 
        tree->root = nullptr;  
        return tree; 
    }

    auto new_node(auto tree, auto value, auto allocator) {
        using TreeVal = decltype(*tree); 
        using TreeDecay = std::decay_t<TreeVal>;
        auto node = allocator.template operator()<typename TreeDecay::Node>(); 
        node->value = value; 
        node->size = 1; 
        node->son[0] = node->son[1] = nullptr; 
        node->parent = nullptr; 
        return node; 
    }

    auto size_impl(auto node) {
        size_t v; 
        if (node == nullptr) {
            v = 0; 
        } else {
            v = node -> size; 
        } 
        return v; 
    }

    auto size(auto tree) {
        return size_impl(tree->root);
    }

    auto instantUpdateSize(auto tree, auto node) {
        node -> size = size_impl(node->son[0]) + size_impl(node->son[1]) + 1;  
        return ; 
    }

    auto rotate_left(auto tree, auto node) { 
        auto son = node -> son[1]; 
        auto grandson = son -> son[0]; 
        son -> son[0] = node; 
        node -> son[1] = grandson; 
        if (grandson != nullptr) {
            grandson -> parent = node; 
        }
        // son -> parent = node -> parent; 
        node -> parent = son; 
        instantUpdateSize(tree, node); 
        instantUpdateSize(tree, son); 
        return son; 
    }

    auto rotate_right(auto tree, auto node) {
        auto son = node -> son[0]; 
        auto grandson = son -> son[1]; 
        son -> son[1] = node; 
        node -> son[0] = grandson; 
        if (grandson != nullptr) {
            grandson -> parent = node; 
        }
        // son -> parent = node -> parent; 
        node -> parent = son; 
        instantUpdateSize(tree, node); 
        instantUpdateSize(tree, son); 
        return son; 
    } 

    auto insert_impl(auto tree, auto node, auto index, auto value, auto allocator) {
        if (node == nullptr) {
            return new_node(tree, value, allocator); 
        } 
        auto left_size = size_impl(node->son[0]); 
        decltype(node) update; 
        if (index <= left_size) {
            update = node->son[0] = insert_impl(tree, node->son[0], index, value, allocator); 
        } else {
            update = node->son[1] = insert_impl(tree, node->son[1], index - left_size - 1, value, allocator); 
        } 
        update -> parent = node; 
        node -> size += 1; 
        auto limitation = node -> size / 4; 
        if (size_impl(node->son[0]) < limitation) {
            node = rotate_left(tree, node); 
        } else if (size_impl(node->son[1]) < limitation) {
            node = rotate_right(tree, node); 
        } 
        return node; 
    }

    auto insert(auto tree, auto index, auto value, auto allocator) {
        tree->root = insert_impl(tree, tree->root, index, value, allocator); 
        tree->root->parent = nullptr; 
    }

    auto insert_last(auto tree, auto value, auto allocator) {
        insert(tree, size(tree), value, allocator); 
    }

    auto insert_first(auto tree, auto value, auto allocator) {
        insert(tree, (size_t ) 0, value, allocator); 
    } 

    auto query_impl(auto tree, auto node, auto idx) {
        auto left_size = size_impl(node->son[0]); 
        if (idx == left_size) {
            return node; 
        } else if (idx < left_size) {
            return query_impl(tree, node->son[0], idx); 
        } else {
            return query_impl(tree, node->son[1], idx - left_size - 1); 
        }     
    }

    auto query(auto tree, auto idx) {
        return query_impl(tree, tree->root, idx) -> value; 
    } 

    auto walk_impl(auto tree, auto node, auto walker) {
        if (node == nullptr) {
            return ; 
        }
        walk_impl(tree, node->son[0], walker);
        walker(node->value);
        walk_impl(tree, node->son[1], walker);
    }

    auto walk(auto tree, auto walker) {
        walk_impl(tree, tree->root, walker); 
    }

    auto height_impl(auto tree, auto node) {
        if (node == nullptr) {
            return 0; 
        }
        auto l = height_impl(tree, node->son[0]) + 1;
        auto r = height_impl(tree, node->son[1]) + 1;  
        if (l > r) {
            return l; 
        } else {
            return r; 
        } 
    }

    auto height(auto tree) {
        return height_impl(tree, tree->root);  
    }

    auto delete_direct_impl(auto tree, auto node, auto ret_val) {
        auto current = node; 
        auto par = node -> parent; 
        if (ret_val != nullptr) {
            *ret_val = node -> value;  
        }
        if (node -> son[0] != nullptr) {
            current = node -> son[0]; 
        } else {
            current = node -> son[1]; 
        }
        if (par == nullptr) {
            tree -> root = current; 
            if (current != nullptr) {
                current -> parent = nullptr; 
            }
        } else {
            if (par -> son[0] == node) {
                par -> son[0] = current; 
            } else {
                par -> son[1] = current; 
            }
            if (current != nullptr) {
                current -> parent = par; 
            } 
        }
        current = par; 
        while (current != nullptr) {
            par = current -> parent; 
            auto to_change = par == nullptr ? &tree -> root : (par -> son[0] == current ? &par -> son[0] : &par -> son[1]); 
            instantUpdateSize(tree, current); 
            auto limitation = current -> size / 4; 
            if (size_impl(current->son[0]) < limitation) {
                current = *to_change = rotate_left(tree, current); 
            } else if (size_impl(current->son[1]) < limitation) {
                current = *to_change = rotate_right(tree, current); 
            } 
            current -> parent = par; 
            current = par; 
        } 
    }

    auto swap_without_value(auto tree, auto node, auto node2) {
        auto node_par = node -> parent; 
        auto node_par_link = node_par == nullptr ? &tree -> root : (node_par -> son[0] == node ? &node_par -> son[0] : &node_par -> son[1]); 
        auto node2_par = node2 -> parent; 
        auto node2_par_link = node2_par == nullptr ? &tree -> root : (node2_par -> son[0] == node2 ? &node2_par -> son[0] : &node2_par -> son[1]); 
        node -> parent = node2_par; 
        *node2_par_link = node; 
        node2 -> parent = node_par; 
        *node_par_link = node2; 
        auto node_sons0 = node -> son[0]; 
        auto node_sons1 = node -> son[1]; 
        node -> son[0] = node2 -> son[0]; 
        node -> son[1] = node2 -> son[1]; 
        node2 -> son[0] = node_sons0; 
        node2 -> son[1] = node_sons1; 
        auto s = node -> size; 
        node -> size = node2 -> size; 
        node2 -> size = s; 
    }

    auto delete_impl(auto tree, auto node, auto ret_val, auto deleter) {
        if (node -> son[0] != nullptr && node -> son[1] != nullptr) {
            auto current = node -> son[1]; 
            while (current -> son[0] != nullptr) {
                current = current -> son[0]; 
            }
            swap_without_value(tree, node, current); 
        }
        delete_direct_impl(tree, node, ret_val); 
        deleter(node); 
    }

    auto delete_at(auto tree, auto index, auto ret_val, auto deleter) {
        auto node = query_impl(tree, tree->root, index); 
        delete_impl(tree, node, ret_val, deleter); 
    }

    auto delete_first(auto tree, auto ret_val, auto deleter) {
        delete_at(tree, (size_t ) 0, ret_val, deleter);  
    }

    auto delete_last(auto tree, auto ret_val, auto deleter) {
        delete_at(tree, size(tree) - 1, ret_val, deleter); 
    }

    auto set_at(auto tree, auto index, auto value) {
        auto node = query_impl(tree, tree->root, index); 
        auto src = node -> value; 
        node -> value = value;  
        return src; 
    }

    auto destroy_impl(auto node, auto deleter) {
        if (node == nullptr) {
            return ; 
        }
        destroy_impl(node->son[0], deleter); 
        destroy_impl(node->son[1], deleter); 
        deleter(node); 
    }

    auto destroy(auto tree, auto deleter) {
        destroy_impl(tree->root, deleter); 
    }

}

namespace ost = order_statistic_tree; 